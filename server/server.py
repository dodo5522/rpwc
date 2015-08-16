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
        self.render("index.html")


class RequestHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        results = []
        api = args[0]
        option = self.get_argument("push_range")

        kwargs["dest_addr_long"] = 0x0013A20040AFBCCE
        kwargs["serial_port"] = "/dev/ttyAMA0"
        kwargs["serial_baurate"] = 9600

        main = rpwc.RemotePowerController()
        main(**kwargs)

        results.append(api + " with " + option + " is done.")
        results.append("The result is " + "...")

        self.render("result.html", results=results)

if __name__ == "__main__":
    application = web.Application(
        [(r"/", MainHandler), (r"/api/(.+)", RequestHandler), ],
        template_path=os.path.join(os.getcwd(), "templates"),
        static_path=os.path.join(os.getcwd(), "static"))

    application.listen(8888)
    print("Server is up....")

    ioloop.IOLoop.instance().start()
