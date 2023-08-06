#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requires = [
    "cytoolz",
    "requests",
]

dev_requires = [
    "pytest",
    "pytest-cov",
    "flake8",
    "autopep8",
    "mypy",
    "pytest-mypy",
    "typing_extensions",
    "twine",
]

setup(
    name="mlboard_client",
    version="0.0.5.rc2",
    description="mlboard client",
    author='Xinyuan Yao',
    author_email='yao.ntno@google.com',
    license="MIT",
    packages=find_packages(),
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    },
    python_requires='>=3.6',
)
