#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages


def requires():
    with open("requiremensts.txt", "r") as fp:
        return [p for p in fp]


setup(
    name='rpwc',
    version='0.0.2',
    description='Remote power controller.',
    author='Takashi Ando',
    url='https://github.com/dodo5522/remote_power_controller',
    py_modules=find_packages(),
    install_requires=requires()
)
