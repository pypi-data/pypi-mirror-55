#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: weijian
@file: douban.py
@date: 2019-11-15
"""

import copy
from bs4 import BeautifulSoup
from ..movie import BasicMovie
from ..api import MovieApi
from colorama import init, Fore, Back, Style
from textwrap import fill


class DoubanApi(MovieApi):
    # session copy用deepcopy
    session = copy.deepcopy(MovieApi.session)
    session.headers.update({"referer": "https://www.douban.com/"})


class DoubanMovie(BasicMovie):
    def __init__(self):
        super(DoubanMovie, self).__init__()


def douban_search(keyword) -> list:
    """
    豆瓣搜索电影：含腾讯视频，爱奇艺，优酷视频，1905电影网等
    """

    movie_list = []

    params = dict(

    )

    resp_search_result_text = DoubanApi.request(
        url="https://www.douban.com/search?q=" + keyword, method="GET", data=params
    )

    movie_detail_url = BeautifulSoup(
        resp_search_result_text, "html.parser").find_all("a", class_="nbg", limit=1)[0].get("href") # 只找第一个
    resp_movie_detail_text = DoubanApi.request(
        url=movie_detail_url, method="GET", data=params
    )
    movie_play_url = BeautifulSoup(resp_movie_detail_text, "html.parser").find_all("a", class_="playBtn")

    for u in movie_play_url:
        movie = DoubanMovie()
        movie.title = keyword
        movie.source = u.get("data-cn")
        movie.url = fill(u.get("href"), width=50)
        if ("".join(u.next_sibling.next_sibling.contents[0].string.split())) == "免费观看":
            movie.pay = Fore.GREEN + "免费" + Fore.RESET
        elif ("".join(u.next_sibling.next_sibling.contents[0].string.split())) == "VIP免费观看":
            movie.pay = Fore.RED + "VIP" + Fore.RESET
        else:
            continue
        movie_list.append(movie)

    return movie_list
