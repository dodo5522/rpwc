#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from flask import Flask, request, render_template, redirect


api = Flask("rpwc_api")


@api.route("/")
def index():
    return render_template("index_api.html")


@api.route("/api/index.hml", methods=["POST", ])
def show_index():
    return redirect("/")


@api.route("/api/pwoff", ["POST", ])
def do_power_off():
    return redirect("/")


@api.route("/api/fcpwoff", ["POST", ])
def do_force_power_off():
    return redirect("/")


if __name__ == "__main__":
    api.run("", port=8087, debug=True)
