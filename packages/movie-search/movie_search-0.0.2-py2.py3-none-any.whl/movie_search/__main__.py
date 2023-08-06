# -*- coding:utf-8 -*-

"""
@author: weijian001
@file: __main__.py
@time: 20191-11-14
"""

import click
import prettytable as pt
from prettytable import ALL as ALL
from movie_search.sources import douban

def format_table(movie_list):
    """
    格式化输出
    """
    # 初始化colorama，并设置自动恢复颜色
    # init(autoreset=True)
    tb = pt.PrettyTable(hrules=ALL)
    tb.field_names = ["来源", "名称", "付费/会员", "下载/观看链接"]
    for movie in movie_list:
        # print(movie)
        tb.add_row(movie.row)
    tb.align = "l"
    print(tb)


def search(keyword):
    movie_list = douban.douban_search(keyword)
    format_table(movie_list)


@click.command()
@click.option("-k", "--keyword", default="厉害了，我的国", help="搜索关键字")
def main(
        keyword,
):
    """
    主入口
    """

    search(keyword)


if __name__ == "__main__":
    main()