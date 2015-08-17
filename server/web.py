#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This module is for... """

import os
import tornado.ioloop as ioloop
import tornado.web as web
import rpwc

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", disabled="", result="")

    def post(self, *args, **kwargs):
        self.render("index.html", disabled="disabled", result="")

        results = []
        push_range = self.get_argument("push_range")

        kwargs["dest_addr_long"] = 0x0013A20040AFBCCE
        kwargs["serial_port"] = "/dev/ttyAMA0"
        kwargs["serial_baurate"] = 9600
        kwargs["interval"] = 1 if push_range == "long" else 1

        pushPowerButton = rpwc.RemotePowerController()
        pushPowerButton(**kwargs)

        results.append("push range is " + push_range)
        results.append("command result is " + "...")

        self.render("index.html", disabled="", result="\n".join(results))


class ApiHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def post(self, *args, **kwargs):
        raise NotImplementedError


if __name__ == "__main__":
    path_here = os.path.dirname(os.path.abspath(__file__))

    application = web.Application(
        [(r"/", MainHandler), (r"/api/(.+)", ApiHandler), ],
        template_path=os.path.join(path_here, "templates"),
        static_path=os.path.join(path_here, "static"))

    application.listen(8888)
    print("Server is up....")

    ioloop.IOLoop.instance().start()
