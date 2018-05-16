#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install using distutils

Run:
    python setup.py install

to install this package.
"""
from setuptools import setup, find_packages
from os.path import join

name = "tmsyscall"
desc = "Python library for some advanced Linux system calls"

with  open('classifiers.txt') as c_file:
    classifiers = c_file.read()

with  open('requirements.txt') as r_file:
    requirements = r_file.read()

with  open('README.rst') as r_file:
    long_desc = r_file.read()


setup(
    name=name,
    version=open(join(name, 'version')).readline().strip("\r\n"),
    description=desc,
    long_description=long_desc,
    author='João Pinto',
    author_email='lamego.pinto@gmail.com',
    classifiers=[x for x in classifiers.splitlines() if x],
    install_requires=[x for x in requirements.splitlines() if x],
    url='https://github.com/joaompinto/'+name,
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts':[name + ' = ' + name + '.__main__:main']},
    #python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
)
