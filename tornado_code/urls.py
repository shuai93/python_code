# coding:utf-8

import os

from handlers import Client
from handlers.BaseHandler import StaticFileHandler

handlers = [
    (r"/api/test", Client.TestHandler),
    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]