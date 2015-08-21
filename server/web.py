#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This module is for... """

import os
import time
import json
import shelve
import configparser
import tornado.ioloop as ioloop
import tornado.web as web
import rpwc

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"


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
    }

    def __init__(self,
                 config_path="/var/tmp/rpwc.conf",
                 db_path="/var/tmp/rpwc.db"):
        self.config = configparser.SafeConfigParser()
        self.db = shelve.open(db_path)

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


class MainHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        web.RequestHandler.__init__(self, *args, **kwargs)

        params = {}
        params["xbee_dest_addr"] = 0x0013A20040AFBCCE
        params["xbee_gpio_power"] = "P0"
        params["serial_port"] = "/dev/ttyAMA0"
        params["serial_baurate"] = 9600

        self.ctrl = rpwc.RemotePowerController(**params)

        self.disabled = ""
        self.result_text = ""
        self.results = []

    def get(self):
        self.render(
            "index.html", disabled=self.disabled, result=self.result_text)

    def post(self, *args, **kwargs):
        push_range = self.get_argument("push_range")
        interval = 5 if push_range == "long" else 1

        self.ctrl.press_power_button(
            callback=self.__on_power_button_pressed)

        if self.ctrl.wait_for_command_done(interval) is not True:
            raise rpwc.TimeoutError("Timeout!!!")

        # FIXME
        time.sleep(interval)

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
        self.results.append(read_frame)

        print("callback is called with " + str(read_frame))
        self.ctrl.set_event()

    def __on_power_button_released(self, read_frame):
        """ Callback function which is called when xbee remote_at command
            finished. """

        # {'status': b'\x00', 'source_addr': b'%Y',
        #  'source_addr_long': b'\x00\x13\xa2\x00@\xaf\xbc\xce',
        #  'frame_id': b'\x01', 'command': b'P0', 'id': 'remote_at_response'}
        self.results.append(read_frame)

        print("callback is called with " + str(read_frame))
        self.ctrl.set_event()

        self.disabled = ""
        self.result_text = "\n".join(str(result) for result in self.results)


class ApiHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        web.RequestHandler.__init__(self, *args, **kwargs)

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "text/plain")
        self.write(json.dumps({"status": "OK", "detail": "none"}))


if __name__ == "__main__":
    config = Configuration()
    print(config.xbee_gpio_power)

    path_here = os.path.dirname(os.path.abspath(__file__))

    application = web.Application(
        [(r"/", MainHandler), (r"/api/(.+)", ApiHandler), ],
        template_path=os.path.join(path_here, "templates"),
        static_path=os.path.join(path_here, "static"))

    application.listen(8888)
    print("Server is up....")

    ioloop.IOLoop.instance().start()
