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
        "console_scripts": [
            "rpwc=rpwc.__main__:main",
            "rpwcweb=rpwc.web.ui:main",
        ],
    },
    packages=find_packages(),
    install_requires=requires(),
    data_files=[
        ("static", ["static/jquery-3.1.1.min.js"]),
        ("static/bootstrap/css", ["static/bootstrap/css/bootstrap.min.css"]),
        ("static/bootstrap/js", ["static/bootstrap/js/bootstrap.min.js"]),
        ("static/mine/css", ["static/mine/css/simple.css"]),
        ("static/mine/js", ["static/mine/js/parts.js"]),
        ("static/sweetalert/css", ["static/sweetalert/css/sweetalert.css"]),
        ("static/sweetalert/js", ["static/sweetalert/js/sweetalert.min.js"]),
        ("templates", ["templates/index.html"]),
        ("templates", ["templates/index_api.html"]),
    ]
)
