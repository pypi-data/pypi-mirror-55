#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

name_ = 'lindh-jsonobject'
github_name = 'jsonobject'
version_ = '1.4.0'
packages_ = [
    'lindh.jsonobject',
]

with open("README.rst", "r") as fh:
    long_description = fh.read()


classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
]

setup(
    name=name_,
    version=version_,
    author='Johan Egneblad',
    author_email='johan@DELETEMEegneblad.se',
    description='JSON serializable objects',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    url='https://github.com/eblade/'+github_name,
    download_url=('https://github.com/eblade/%s/archive/v%s.tar.gz'
                  % (github_name, version_)),
    packages=packages_,
    install_requires=[],
    classifiers=classifiers,
)
