#!/usr/bin/env python3  
# @Time    : 18-2-5 上午11:21
# @Author  : ys
# @Email   : youngs@yeah.net

from sanic import Sanic
from sanic.response import json, text, redirect
from sanic.views import HTTPMethodView

import sanic.request as HttpRequest
import base64

app = Sanic(__name__)


@app.route("/test")
async def test(request: HttpRequest):

    print(request)
    return json({"hello": "world"})


@app.route("/redirect")
async def test(request: HttpRequest):
    url = app.url_for('SimpleView')
    return redirect(url)


@app.route("/files", methods=["POST"])
def post_json(request):
    test_file = request.files.get('test')

    file_parameters = {
        'body': base64.b64encode(test_file.body),
        'name': test_file.name,
        'type': test_file.type,
    }
    print(file_parameters)
    return json({"received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters})


class SimpleView(HTTPMethodView):

    def get(self, request):
      return text('I am get methodGGGGGGGGGGGGGg')

    def post(self, request):
      return text('I am post method')

    def put(self, request):
      return text('I am put method')

    def patch(self, request):
      return text('I am patch method')

    def delete(self, request):
      return text('I am delete method')


app.add_route(SimpleView.as_view(), '/')


def main():
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
