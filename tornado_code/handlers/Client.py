# coding:utf-8

from .BaseHandler import BaseHandler


class TestHandler(BaseHandler):
    """"""
    def get(self):

        self.write({"code": 0, "message": 'hello'})

