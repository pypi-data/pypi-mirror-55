#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='python-notazz',
    version='0.1',
    description="Notazz Python Binding",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    author='Joao Carvalho',
    author_email='joao.carvalho@maestrus.com',
    install_requires=[
        "requests>=2.22.0",
        "urllib3>=1.25.6",
    ],
    url='https://maestrus.com',
    packages=find_packages(),
)
