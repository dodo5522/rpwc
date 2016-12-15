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
from rpwc.rpwc import push_button
from serial.serialutil import SerialException
import json
import shelve

button_params = {
    "serial_port": "/dev/ttyAMA0",
    "serial_baurate": 9600,
    "xbee_dest_addr": "0x0013A20040AFBCCE",
    "xbee_gpio_power": "P0",
}

application = Flask(
    "rpwc_web_application",
    template_folder="/var/tmp/rpwcweb/templates",
    static_folder="/var/tmp/rpwcweb/static")


@application.route("/")
def index():
    """ top page. """
    with shelve.open("/var/tmp/rpwcweb/contents.db") as db:
        # results = db.get("results", [])
        results = ["This\n", "is a\n", "sample response.\n"]

    return render_template(
        "index.html",
        results=results,
        status="success",
        message="test message")


@application.template_filter("nl2br")
def filter_nl2br(s):
    return escape(s).replace("\n", Markup("<br>"))


@application.route("/api")
def index_api():
    return render_template("index_api.html")


@application.route("/api/pwoff", methods=["POST", "GET"])
def do_power_off():
    try:
        res = push_button(**button_params, interval=1)
    except (SerialException, ):
        res = (False, )

    if False in res:
        return json.dumps({"result": "Failed"})
    else:
        return json.dumps({"result": "OK"})


@application.route("/api/fcpwoff", methods=["POST", "GET"])
def do_force_power_off():
    try:
        res = push_button(**button_params, interval=5)
    except (SerialException, ):
        res = (False, )

    if False in res:
        return json.dumps({"result": "Failed"})
    else:
        return json.dumps({"result": "OK"})


def main(bind="localhost", port=8088, debug=True):
    application.run(bind, port, debug)


if __name__ == "__main__":
    main()
