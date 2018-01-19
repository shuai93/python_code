#!/usr/bin/env python3  
# @Time    : 18-1-19 下午3:47
# @Author  : ys
# @Email   : youngs@yeah.net

import json

from pprint import pprint
from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body


def main():
    url = 'http://api.alpha.yusiontech.com:8000/api/crm/dealer/get_vehicle_model_list?trix_id=1100&vehicle_cond=新车'
    result = synchronous_fetch(url)
    pprint(result)
    # pprint(result.header)

    pprint(json.loads(result))


if __name__ == "__main__":
    main()
