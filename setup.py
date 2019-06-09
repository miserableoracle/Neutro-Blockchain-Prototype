"""this file is executed with "pip install ."" and installs the Neutro Command Line Interface"""
from codecs import open
from os.path import abspath, dirname, join
from setuptools import Command, find_packages, setup
from neutro import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='Neutro',
    version=__version__,
    description='Client for the Neutro Blockchain Prototype',
    long_description=long_description,
    url='https://github.com/spacesoft-llc/Neutro-Blockchain-Prototype',
    author='Spacesoft LLC',
    author_email='contact@neutro.io',
    license='MIT',
    classifiers=[
        'Intended Audience :: Everyone',
        'Topic :: Cryptocurrency',
        'License :: MIT',
        'Natural Language :: English',
        'Operating System :: Ubuntu',
        'Programming Language :: Python :: 3.x',
    ],
    keywords='Blockchain, Cryptocurrency, Neutro, NTO, Spacesoft LLC',
    packages=find_packages(exclude=['doc', 'tests*']),
    install_requires=['docopt', 'web3', 'base58', 'AtomicP2P'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'neutro=neutro.src.cli.cli:main',
        ],
    }
)
