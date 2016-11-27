#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages


def requires():
    with open("requirements.txt", "r") as fp:
        return [p for p in fp]


setup(
    name='rpwc',
    version='0.0.3',
    description='Remote power controller.',
    license="Apache Software License",
    author='Takashi Ando',
    url='https://github.com/dodo5522/rpwc',
    entry_points={
        "console_scripts": ["rpwc=rpwc.__main__:main"],
    },
    packages=find_packages(),
    install_requires=requires()
)
