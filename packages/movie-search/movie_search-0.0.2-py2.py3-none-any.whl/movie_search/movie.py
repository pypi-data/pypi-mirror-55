#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: weijian
@file: movie.py
@date: 2019-11-15
"""

import logging


"""
    Basic Movie Object
"""


class BasicMovie:

    def __init__(self):
        self.id = 0
        self.title = ""
        self.director = ""
        self.star = []
        self.time = 0
        self.source = ""
        self.pay = "-"
        self.url = ""
        self.logger = logging.getLogger(__name__)

    @property
    def row(self) -> list:
        return [
            self.source,
            self.title,
            self.pay,
            self.url
        ]




