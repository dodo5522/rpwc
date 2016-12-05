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
from rpwc import rpwc
import json
import serial
import shelve
import time


application = Flask("rpwc_web_application")


def get_buttons(serial_port="/dev/ttyAMA0", serial_baurate=9600, dest="0x0013A20040AFBCCE", gpio="P0"):
    pressing_button = None
    releasing_button = None

    ser_obj = serial.Serial(serial_port, serial_baurate)
    pressing_button = rpwc.ZigbeeCommander(
        ser_obj,
        dest,
        gpio,
        rpwc.ZigbeeCommander.CMD_PARAM_HIGH)
    releasing_button = rpwc.ZigbeeCommander(
        ser_obj,
        dest,
        gpio,
        rpwc.ZigbeeCommander.CMD_PARAM_LOW)

    return (pressing_button, releasing_button)


def push_button(interval):
    (pressing_button, releasing_button) = get_buttons()

    pressing_button.put()
    pressing_button.wait()

    time.sleep(interval)

    releasing_button.put()
    releasing_button.wait()

    return [pressing_button.is_ok(), releasing_button.is_ok()]


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
    if False in push_button(1):
        return json.dumps({"result": "Failed"})
    else:
        return json.dumps({"result": "OK"})


@application.route("/api/fcpwoff", methods=["POST", "GET"])
def do_force_power_off():
    if False in push_button(5):
        return json.dumps({"result": "Failed"})
    else:
        return json.dumps({"result": "OK"})


if __name__ == "__main__":
    application.run("", port=8088, debug=True)
