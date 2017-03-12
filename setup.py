#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '1.1.0'

with open('README.rst') as f:
    long_description = f.read()

with open('LICENSE') as f:
    long_license = f.read()

setup(
    name='pystructure',
    version=VERSION,
    description="a simple tool to show code structure about python source code",
    long_description=long_description,
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='pystructure structure ast',
    author='hanks',
    author_email='zhouhan315@gmail.com',
    url='https://github.com/hanks/pystructure',
    license=long_license,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'docopt>=0.6.2',
    ],
    entry_points={
        'console_scripts': [
            'pystructure = pystructure:main'
        ]
    },
)