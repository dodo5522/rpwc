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

from flask import Flask, request, render_template, redirect, escape, Markup
import shelve


application = Flask("rpwc_web_application")


@application.route("/")
def index():
    """ top page. """
    with shelve.open("/var/tmp/rpwcweb/contents.db") as db:
        # results = db.get("results", [])
        results = ["aaaa\n", "bbbb\n", "cccc\n"]

    return render_template(
        "index.html",
        disabled="",
        results=results,
        status="success",
        message="test message")


@application.route("/post", methods=["POST", ])
def post():
    """ post form page. """
    return redirect("/")


@application.template_filter("nl2br")
def filter_nl2br(s):
    return escape(s).replace("\n", Markup("<br>"))


if __name__ == "__main__":
    application.run("", port=8088, debug=True)
