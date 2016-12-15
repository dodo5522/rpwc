#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os
import re


def get_install_dir(relative_path):
    regex = re.compile("HTDOC_ROOT_PATH=.+")
    install_dir = "/var/tmp"

    with open("etc/default/rpwcweb") as f:
        for line in f.readlines():
            m = regex.search(line)
            if m:
                install_dir = os.path.join(
                    m.group(0).split("=")[1], relative_path)
                break

    return install_dir


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
        "console_scripts": [
            "rpwc=rpwc.__main__:main",
            "rpwcweb=rpwc.web.ui:main",
        ],
    },
    packages=find_packages(),
    install_requires=requires(),
    data_files=[
        (get_install_dir("static"), ["static/jquery-3.1.1.min.js"]),
        (get_install_dir("static/bootstrap/css"), ["static/bootstrap/css/bootstrap.min.css"]),
        (get_install_dir("static/bootstrap/js"), ["static/bootstrap/js/bootstrap.min.js"]),
        (get_install_dir("static/mine/css"), ["static/mine/css/simple.css"]),
        (get_install_dir("static/mine/js"), ["static/mine/js/parts.js"]),
        (get_install_dir("static/sweetalert/css"), ["static/sweetalert/css/sweetalert.css"]),
        (get_install_dir("static/sweetalert/js"), ["static/sweetalert/js/sweetalert.min.js"]),
        (get_install_dir("templates"), ["templates/index.html", "templates/index_api.html"]),
    ]
)
