#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name='rpwc',
    version='0.0.1',
    description='Remote power controller.',
    author='Takashi Ando',
    url='https://github.com/dodo5522/remote_power_controller',
#    packages=[
#        "driver"],
    py_modules=[
        "rpwc"],
    install_requires=[
        "pyserial>=2.5",
        "XBee>=2.1.0"]
)
