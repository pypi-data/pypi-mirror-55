#!/usr/bin/env python
from setuptools import setup

setup(
    name='onlykey_agent',
    version='1.0.0',
    description='Using OnlyKey as hardware SSH agent',
    author='CryptoTrust',
    author_email='admin@crp.to',
    url='http://github.com/trustcrypto/onlykey-agent',
    packages=['onlykey_agent'],
    install_requires=['ecdsa>=0.13', 'ed25519>=1.4', 'Cython>=0.23.4', 'protobuf>=2.6.1', 'semver>=2.2'],
    platforms=['POSIX'],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Communications',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    entry_points={'console_scripts': [
        'onlykey-agent = onlykey_agent.__main__:run_agent',
    ]},
)
