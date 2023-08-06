#/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: weijian
@file: api.py
@date: 2019-11-15
"""

import requests

class MovieApi:

    session = requests.Session()
    # 跨请求参数
    # ...

    @classmethod
    def request(cls, url, method="POST", data=None):
        if method == "GET":
            resp = cls.session.get(url, params=data, timeout=7)
        else:
            resp = cls.session.get(url, params=data, timeout=7)

        if resp.status_code != requests.codes.ok:
            raise RuntimeError

        return resp.text