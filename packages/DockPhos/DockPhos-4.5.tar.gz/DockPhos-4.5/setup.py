import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='DockPhos',
    version='4.5',
    author='SDC-CH',
    author_email='sdc-ch@unige.ch',
    description='Helper script for using the Phosphoros Docker container',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.euclid-sgs.uk//SDC-CH/SDCCH_DockerPhosphoros',
    py_modules=['DockPhos'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta'
    ],
    python_requires='>=3.1',
    entry_points={
        'console_scripts': [
            'DockPhos = DockPhos:main_func'
        ]
    },
    install_requires=[
        'coloredlogs',
        'requests',
        'packaging',
    ]
)
