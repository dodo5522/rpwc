#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This module is for... """

import os
import tornado.ioloop as ioloop
import tornado.web as web
import rpwc

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"


class ApiHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def post(self, *args, **kwargs):
        raise NotImplementedError

class MainHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self, *args, **kwargs):
        results = []
        api = args[0]
        option = self.get_argument("push_range")

        kwargs["dest_addr_long"] = 0x0013A20040AFBCCE
        kwargs["serial_port"] = "/dev/ttyAMA0"
        kwargs["serial_baurate"] = 9600
        kwargs["interval"] = 1

        main = rpwc.RemotePowerController()
        main(**kwargs)

        results.append(api + " with " + option + " is done.")
        results.append("The result is " + "...")

        self.render("result.html", results=results)

if __name__ == "__main__":
    path_here = os.path.dirname(os.path.abspath(__file__))

    application = web.Application(
        [(r"/", MainHandler), (r"/api/(.+)", ApiHandler), ],
        template_path=os.path.join(path_here, "templates"),
        static_path=os.path.join(path_here, "static"))

    application.listen(8888)
    print("Server is up....")

    ioloop.IOLoop.instance().start()
