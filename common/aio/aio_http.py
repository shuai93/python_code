#!/usr/bin/env python3  
# @Time    : 18-1-22 下午5:40
# @Author  : ys
# @Email   : youngs@yeah.net

import json
import time

from aiohttp import web
from functools import wraps, partial

dumps = partial(json.dumps, indent=4)


def permission_authentication():
    def func_wrapper(func):
        @wraps(func)
        async def _wrapper(request, *args, **kwargs):
            token = request.headers.get("authentication")
            if token:
                token = token.split(" ")[-1]
                print(token)
                try:
                    if token == "112358":
                        result = await func(request, *args, **kwargs)
                        return result
                    else:
                        body = json.dumps({'code': -1, 'msg': '登录信息错误'}, ensure_ascii=False)
                        result = web.Response(body=body)
                        result.headers.add("Content-Type", "application/json")
                        # result.headers.add("Access-Control-Allow-Origin", "*")
                        return result
                except Exception as e:
                    return web.Response(body=json.dumps({'code': -1, 'msg': '登录信息错误', "error": e}, ensure_ascii=False))
            else:
                return web.Response(body=json.dumps({'code': -1, 'msg': '登录信息错误'}, ensure_ascii=False))
        return _wrapper
    return func_wrapper


def permission(func):
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
    return wrapper


@permission_authentication()
async def index(request):
    print(request.headers.get("authentication"))
    # return web.Response(text='hello world')
    return web.json_response({"code": 0, "msg": "hello world"}, dumps=dumps)


def main():
    app = web.Application()
    app.router.add_get('/', index)
    web.run_app(app, port=8080)

if __name__ == "__main__":
    main()
