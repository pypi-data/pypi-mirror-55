#!/usr/bin/env python3
from __future__ import print_function

import getpass
import json
import logging
import os
import subprocess
import sys
import tempfile
from argparse import ArgumentParser

import pkg_resources
import requests
from packaging.version import Version

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

PACKAGE_NAME = 'DockPhos'
log = logging.getLogger(PACKAGE_NAME)

try:
    __version__ = Version(pkg_resources.require(PACKAGE_NAME)[0].version)
except pkg_resources.DistributionNotFound:
    __version__ = Version('99')


class RSAKeyPair(object):
    def __init__(self, basedir=None):
        if basedir is None:
            if sys.platform == 'darwin':
                # Latest MacOSX seem to put tempdir somewhere in /var, which is not accessible
                # by Docker for Mac
                tempdir = '/private/tmp'
            else:
                tempdir = tempfile.gettempdir()
            basedir = os.path.join(tempdir, getpass.getuser(), 'phosphoros')

        self.__dir = basedir
        self.private_key = os.path.join(self.__dir, 'phosphoros.rsa')
        self.public_key = os.path.join(self.__dir, 'phosphoros.rsa.pub')

    def create(self):
        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        try:
            # Crypto library has a bug in Python3 that does not allow to get the
            # public ssh key. For this reason we throw an exception to force the
            # use of the ssh-keygen
            if sys.version_info[0] == 3:
                raise ImportError()
            from Crypto.PublicKey import RSA
            key = RSA.generate(2048)
            with open(self.private_key, 'w') as key_file:
                key_file.write(key.exportKey('PEM'))
            with open(self.public_key, 'w') as key_file:
                key_file.write(key.publickey().exportKey('OpenSSH'))
        except ImportError:
            # Crypto package is not available. Use ssh-keygen
            cmd = ['ssh-keygen', '-t', 'rsa', '-N', '', '-f', self.private_key]
            log.debug(cmd)
            subprocess.call(cmd)
        os.chmod(self.private_key, 0o600)
        os.chmod(self.public_key, 0o640)
        return self


class DockerContainer(object):

    def _run_cmd(self, cmd, **kwargs):
        log.debug(cmd)
        output = subprocess.check_output(cmd, **kwargs).strip().decode()
        log.debug(output)
        return output

    def _reload(self):
        try:
            self.ip = self._run_cmd(['docker-machine', 'ip'])
            log.info('Running in Docker Machine')
            self.is_docker_machine = True
        except:
            self.ip = 'localhost'
            self.is_docker_machine = False
        self.id = self._run_cmd(['docker', 'ps', '-af', 'name=' + self.name, '-q'])
        if self.id:
            self.__info = json.loads(self._run_cmd(['docker', 'inspect', self.name]))[0]
        else:
            self.__info = None

    def __init__(self, name):
        self.name = name
        self._reload()

    @property
    def ssh_port(self):
        return self.__info['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']

    @property
    def phosphoros_root(self):
        return [m for m in self.__info['Mounts'] if m['Destination'] == '/Phosphoros'][0]['Source']

    @property
    def mounts(self):
        return map(
            lambda m: (m['Source'], m['Destination']),
            filter(lambda m: m['Destination'].startswith('/mount'), self.__info['Mounts'])
        )

    @property
    def running(self):
        return self.__info is not None and self.__info['State']['Running']

    @property
    def exists(self):
        return self.__info is not None

    def stop(self):
        self._run_cmd(['docker', 'stop', self.name], stderr=subprocess.STDOUT)
        self._reload()

    def rm(self):
        self._run_cmd(['docker', 'rm', self.name], stderr=subprocess.STDOUT)
        self._reload()

    def start(self):
        assert self.exists and not self.running
        cmd = ['docker', 'start', self.name]
        self._run_cmd(cmd)
        self._reload()

    def run(self, image, uid, gid, volumes, ports, daemon):
        cmd = ['docker', 'run', '--name', self.name, '-d',
               '-e', 'DEV_UID=' + str(uid), '-e', 'DEV_GID=' + str(gid)]

        for local_dir, mount_dir in volumes:
            cmd += ['-v', '{}:{}:Z'.format(local_dir, mount_dir)]

        for port in ports:
            cmd += ['-p', str(port)]

        cmd += ['-e', 'USER=root', '-u', 'root', image]
        self._run_cmd(cmd)
        self._reload()


class Command(object):
    def register_arguments(self, parser):
        pass


class StatusCommand(Command):
    description = 'Get the info of the running Phosphoros docker container'

    def __call__(self, args):
        container = DockerContainer(args.name)
        if container.running:
            print('Phosphoros docker container is RUNNING')
            print('Container ID:', container.id)
            print('Container IP:', container.ip)
            print('Container ssh port:', container.ssh_port)
            print('Mounted Phosphoros directory:', container.phosphoros_root)
            other_mounts = container.mounts
            if other_mounts:
                print('Other mounted directories:')
                for m in other_mounts:
                    print('  ', m[0], '->', m[1])
        elif container.exists:
            print('Phosphoros docker container is STOPPED')
        else:
            print('Phosphoros docker container is MISSING')


class StopCommand(Command):
    description = 'Stop the Phosphoros docker container'

    def __call__(self, args):
        container = DockerContainer(args.name)
        if container.running:
            print('Stopping existing Phosphoros docker container...')
            container.stop()
        elif container.exists:
            print('The Phosphoros container is not running')
        else:
            print('The Phosphoros container does not exist')


class StartCommand(Command):
    description = 'Start the Phosphoros docker container in the background'

    def register_arguments(self, parser):
        parser.add_argument('-d', '--phos_dir', metavar='PHOS_DIR', type=str,
                            help='The Phosphoros root directory to use')
        parser.add_argument('-v', '--phos_version', metavar='PHOS_VER', type=str, default='latest',
                            help='The Phosphoros version to run (default latest)')
        parser.add_argument('-l', '--phos_label', metavar='PHOS_LABEL', type=str, default='topcat',
                            choices=['cli', 'light', 'full', 'topcat'],
                            help='The Phosphoros label to run, one of cli, light, full, topcat')
        parser.add_argument('-m', '--mount', metavar='MOUNT', action='append', nargs='+', default=[],
                            help='A list of local directories to mount')
        parser.add_argument('-p', '--ssh_port', type=int, default=22,
                            help='Fix the port of the host to use for ssh')
        parser.add_argument('-f', '--force-update', action='store_true',
                            help='Remove existing container, if any, and pull from remote')
        parser.add_argument('--no_pull', action='store_true', help='Always use the local image')

    def _get_mounts(self, mount):
        mounts = []
        for m in mount:
            m = m.split(':')
            if not os.path.isdir(m[0]):
                raise NotADirectoryError('ERROR: Cannot mount', m[0], 'because it is not a directory')
            absdir = os.path.abspath(m[0])
            mountdir = '/mount';
            if len(m) > 1:
                if len(m[1]) == 0:
                    raise ValueError('ERROR: Empty mount name for directory', m[0])
                mountdir += '/' + m[1]
            else:
                mountdir += absdir
            log.info('Directory', absdir, 'will be mounted under', mountdir)
            mounts.append((absdir, mountdir))
        return mounts

    def _get_root_path(self, root_path):
        if not root_path:
            root_path = os.environ.get('PHOSPHOROS_ROOT', os.path.expanduser('~/Phosphoros'))

        root_path = os.path.abspath(root_path)

        if not os.path.exists(root_path):
            while True:
                create = input('Phosphoros root directory ' + root_path + ' does not exist.' +
                               ' Should I create it? (yes/no): ')
                if create == 'no':
                    raise FileNotFoundError('ERROR: Phosphoros root directory', root_path,
                                            'does not exist. Please create it before using the',
                                            __file__, 'script, or use the -d option.')
                if create == 'yes':
                    os.makedirs(root_path)
                    break
        elif not os.path.isdir(root_path):
            raise NotADirectoryError(root_path, ' is not a directory')

        log.info('Using %s as Phosphoros root directory', root_path)
        return root_path

    def __call__(self, args):
        image_name = 'phosphoros/phosphoros.{}:{}'.format(args.phos_label, args.phos_version)
        mounts = self._get_mounts(args.mount)
        phos_root = self._get_root_path(args.phos_dir)

        log.info('Creating RSA key for ssh communication...')
        rsa = RSAKeyPair(args.temp_dir)
        if not os.path.exists(rsa.private_key):
            rsa.create()

        log.info('Starting new Phosphoros docker container...')
        container = DockerContainer(args.name)

        if container.exists and args.force_update:
            log.info('Removing existing container')
            container.rm()

        if container.exists:
            container.start()
        else:
            if not args.no_pull:
                log.info('Checking if local Phosphoros docker image is out of date...')
                cmd = ['docker', 'pull', image_name]
                if subprocess.call(cmd) != 0:
                    log.warning('WARNING: Could not pull the image from the remote repository')
            else:
                log.warning('Not pulling from Docker Hub!')

            if container.is_docker_machine:
                uid, gid = 1000, 50
            else:
                uid, gid = os.getuid(), os.getgid()

            container.run(
                image_name,
                uid=uid, gid=gid,
                volumes=[
                            (phos_root, '/Phosphoros'),
                            (rsa.public_key, '/phosphoros.rsa.pub')
                        ] + mounts,
                daemon=True,
                ports=[args.ssh_port]
            )
        print('Phosphoros container started with ID', container.id)


class ConnectCommand(Command):
    description = 'Open a terminal to the Phosphoros docker container'

    def __call__(self, args):
        container = DockerContainer(args.name)
        rsa = RSAKeyPair(args.temp_dir)
        if not container.running:
            raise RuntimeError('Phosphoros docker container is not running. Run "' + __file__ + ' start" first.')
        log.info('Connecting to Phosphoros docker container..')
        cmd = ['ssh', '-i', rsa.private_key,
               '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no',
               '-Y', 'phosphoros@' + container.ip, '-p', container.ssh_port]
        log.debug(cmd)
        subprocess.call(cmd)


class RemoveCommand(Command):
    description = 'Remove the docker container, but not the images'

    def __call__(self, args):
        container = DockerContainer(args.name)
        if not container.exists:
            raise RuntimeError('Phosphoros docker container does not exist')
        if container.running:
            raise RuntimeError('Phosphoros docker container is running. Stop it first')
        print('Removing existing Phosphoros docker container...')
        container.rm()


class CleanupCommand(Command):
    description = 'Remove any local copies of the docker images'

    def __call__(self, args):
        log.info('Stopping and removing container')
        container = DockerContainer(args.name)
        try:
            container.stop()
            container.rm()
        except:
            pass
        cont_id_list = subprocess.check_output(['docker', 'images', 'phosphoros/*', '-q']).strip().decode().split()
        for cont_id in cont_id_list:
            log.info('Removing image %s', cont_id)
            subprocess.call(['docker', 'rmi', cont_id])


class VersionsCommand(Command):
    description = 'List all the available versions'

    def _get_fs_layers(self, repo, tag):
        login_template = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull'
        get_manifest_template = 'https://registry.hub.docker.com/v2/{repository}/manifests/{tag}'
        # First we get the token for authorization
        response = requests.get(login_template.format(repository=repo), json=True)
        response_json = response.json()
        token = response_json["token"]
        # Now we can retrieve the manifest and extract the fs layers
        response = requests.get(
            get_manifest_template.format(repository=repo, tag=tag),
            headers={"Authorization": "Bearer {}".format(token)},
            json=True
        )
        manifest = response.json()
        return manifest['fsLayers']

    def __call__(self, args):
        log.info('Retrieving version information from DockerHub')
        url = 'https://registry.hub.docker.com/v2/repositories/phosphoros/phosphoros.topcat/tags'
        ver_list = {}
        while url is not None:
            data = requests.get(url, json=True).json()
            for info in data['results']:
                tag = info['name']
                ver_list[tag] = self._get_fs_layers('phosphoros/phosphoros.topcat', tag)
            url = data['next']
        # Find which release is the latest
        latest = ''
        for k, v in ver_list.items():
            if k == 'latest':
                continue
            if v == ver_list['latest']:
                latest = k
        # Now we can print the list
        print('Available versions:')
        print('   latest (' + latest + ')')
        vers = list(ver_list.keys())
        vers.remove('latest')
        for v in sorted(vers):
            print('  ', v)


class LabelCommand(Command):
    description = 'List all the available label options'

    def __call__(self, args):
        url = 'https://registry.hub.docker.com/v2/repositories/phosphoros/'
        labels = []
        while url is not None:
            data = requests.get(url, json=True).json()
            for info in data['results']:
                c, l = info['name'].split('.')
                if c == 'phosphoros':
                    labels.append(l)
            url = data['next']
        print('Available labels:')
        for l in labels:
            print('  ', l)


class VersionCommand(Command):
    description = 'Print the script version'

    def __call__(self, args):
        print(__version__)


def check_update(url):
    log.debug(f'Checking if there is an update available in {url}')
    found_version = None

    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        found_version = Version(r.json()['info']['version'])
        log.debug(f'Found version {found_version}')
    except Exception as e:
        log.debug(f'Failed to check for updates: {e}')

    return found_version


def register_command(subparsers, title, command):
    subparser = subparsers.add_parser(title, description=command.description)
    command.register_arguments(subparser)
    subparser.set_defaults(callable=command)


def main_func():
    # Main parser
    parser = ArgumentParser(description='Helper script for using Phosphoros Docker Images')
    parser.add_argument('-d', '--debug', action='store_true', help='Verbose output')
    parser.add_argument('-n', '--name', type=str, default='phosphoros' + '_' + getpass.getuser(), help='Container name')
    parser.add_argument('--temp_dir', type=str, default=None, help='Temporary directory')
    parser.add_argument(
        '--update-url', type=str,
        default=f'https://pypi.org/pypi/{PACKAGE_NAME}/json',
        help='Update endpoint'
    )

    subparsers = parser.add_subparsers()

    register_command(subparsers, 'status', StatusCommand())
    register_command(subparsers, 'stop', StopCommand())
    register_command(subparsers, 'start', StartCommand())
    register_command(subparsers, 'connect', ConnectCommand())
    register_command(subparsers, 'remove', RemoveCommand())
    register_command(subparsers, 'cleanup', CleanupCommand())
    register_command(subparsers, 'versions', VersionsCommand())
    register_command(subparsers, 'labels', LabelCommand())
    register_command(subparsers, 'version', VersionCommand())

    args = parser.parse_args()
    if not hasattr(args, 'callable'):
        parser.print_help()
        sys.exit(1)

    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    if coloredlogs:
        coloredlogs.install(level=log_level)
    else:
        log.setLevel(log_level)
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(log_level)
        log.addHandler(handler)

    # Test for updates
    if args.update_url is not None:
        new_version = check_update(args.update_url)
        if new_version is not None and new_version > __version__:
            log.warning(f'New version available: {new_version} (version {__version__} installed)')

    # Call command'List all the available label options'
    try:
        args.callable(args)
    except Exception as e:
        if args.debug:
            raise
        log.error(str(e))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main_func())
