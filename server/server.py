#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This module is for... """

import os
import tornado.ioloop as ioloop
import tornado.web as web

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        body = self.get_argument("text_for_count")
        len_body = len(body)
        self.render("result.html", len_body=len_body)

application = web.Application(
    [(r"/", MainHandler),],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static"))

if __name__ == "__main__":
    application.listen(8888)
    print("Server is up....")
    ioloop.IOLoop.instance().start()
