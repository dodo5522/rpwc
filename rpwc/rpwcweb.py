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

import os
import time
import json
import shelve
import configparser
import tornado.ioloop as ioloop
import tornado.web as web
import rpwc


class Configuration(object):
    DEFAULT_CONFIG = {
        "xbee": {
            "dest_addr": "0x0013A20040AFBCCE",
            "gpio_power": "P0",
        },
        "serial": {
            "port": "/dev/ttyAMA0",
            "baurate": 9600,
        },
        "general": {
            "path_db": "/var/tmp/rpwcweb/contents.db",
            "path_docroot": "/var/tmp/rpwcweb/docroot",
        }
    }

    def __init__(self, config_path="/etc/rpwcweb/setup.conf"):
        self.config = configparser.SafeConfigParser()

        if os.path.isfile(config_path):
            self.config.read(config_path)
        else:
            self.__write_default_config(config_path)

    def __write_default_config(self, config_path):
        for section in self.DEFAULT_CONFIG.keys():
            self.config.add_section(section)

            for option in self.DEFAULT_CONFIG[section]:
                self.config.set(
                    section, option, str(self.DEFAULT_CONFIG[section][option]))

        with open(config_path, "w") as fp:
            self.config.write(fp)

    def __get_section_from_attr(self, name):
        return name.split("_")[0]

    def __get_option_from_attr(self, name):
        return "_".join(name.split("_")[1:])

    def __getattr__(self, name):
        section = self.__get_section_from_attr(name)
        option = self.__get_option_from_attr(name)

        return self.config.get(section, option)

    def get_attr_names(self):
        return ["_".join((section, option))
                for section in self.DEFAULT_CONFIG
                for option in self.DEFAULT_CONFIG[section]]


class MainHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        web.RequestHandler.__init__(self, *args, **kwargs)

        self.config = Configuration()
        params = {key: getattr(self.config, key)
                  for key in self.config.get_attr_names()}

        self.ctrl = None if __debugging__ else rpwc.RemotePowerController(
            **params)

    def get(self):
        db = shelve.open(self.config.general_path_db)
        results = db.get("results")
        self.render("index.html",
                    disabled="",
                    result="\n".join([] if results is None else
                                     [str(result) for result in results]),
                    # "success", "info", "warning" or "danger"
                    status="success" if 1 else "info",
                    message="test message")
        db.close()

    def post(self, *args, **kwargs):
        push_range = self.get_argument("push_range")
        interval = 5 if push_range == "long" else 1

        if self.ctrl:
            self.ctrl.press_power_button(
                callback=self.__on_power_button_pressed)

            if self.ctrl.wait_for_command_done(interval) is not True:
                raise rpwc.TimeoutError("Timeout!!!")

        # FIXME: this sleep is not exact interval
        time.sleep(interval)

        if self.ctrl:
            self.ctrl.release_power_button(
                callback=self.__on_power_button_released)

            if self.ctrl.wait_for_command_done(interval) is not True:
                raise rpwc.TimeoutError("Timeout!!!")

        self.redirect("/")

    def __on_power_button_pressed(self, read_frame):
        """ Callback function which is called when xbee remote_at command
            finished. """

        # {'status': b'\x00', 'source_addr': b'%Y',
        #  'source_addr_long': b'\x00\x13\xa2\x00@\xaf\xbc\xce',
        #  'frame_id': b'\x01', 'command': b'P0', 'id': 'remote_at_response'}
        db = shelve.open(self.config.general_path_db)
        if db.get("results") is None:
            db["results"] = []
        results = db["results"]
        results.append(read_frame)
        db["results"] = results
        db.close()

        if self.ctrl:
            print("callback is called with " + str(read_frame))
            self.ctrl.set_event()

    def __on_power_button_released(self, read_frame):
        """ Callback function which is called when xbee remote_at command
            finished. """

        # {'status': b'\x00', 'source_addr': b'%Y',
        #  'source_addr_long': b'\x00\x13\xa2\x00@\xaf\xbc\xce',
        #  'frame_id': b'\x01', 'command': b'P0', 'id': 'remote_at_response'}
        db = shelve.open(self.config.general_path_db)
        if db.get("results") is None:
            db["results"] = []
        results = db["results"]
        results.append(read_frame)
        db["results"] = results
        db.close()

        if self.ctrl:
            print("callback is called with " + str(read_frame))
            self.ctrl.set_event()


class ApiHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        web.RequestHandler.__init__(self, *args, **kwargs)

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "text/plain")
        self.write(json.dumps({"status": "OK", "detail": "none"}))

path_contents = Configuration().general_path_docroot
app = web.Application(
    [(r"/", MainHandler), (r"/api/(.+)", ApiHandler), ],
    template_path=os.path.join(path_contents, "templates"),
    static_path=os.path.join(path_contents, "static"))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="only for test.")
    parser.add_argument(
        "-p", "--port",
        type=int,
        metavar="P",
        default=8888,
        help="port number which is listened by rpcweb")
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        default=False,
        help="not to access serial port if true")

    args = parser.parse_args()
    __debugging__ = args.debug

    # config = Configuration()
    # print(config.get_attr_names())

    app.listen(args.port)
    print("Server is up with port {}....".format(args.port))

    ioloop.IOLoop.instance().start()
