#!/usr/bin/python
from setuptools import setup, find_packages
#from swift import __canonical_version__ as version

name = 'monga_client'

setup(
    name=name,
    version='1.0.5',
    description='Crusher Stupid Questions',
    license='Apache License (2.0)',
    author='Promise, LLC.',
    author_email='joeyang@tw.promise.com',
    url='https://www.promise.com.tw/',
    packages=find_packages(exclude=['test', 'bin']),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)',
        ],
    install_requires=[],  # removed for better compat
    scripts=[
    ],
    entry_points={
        },
    )
