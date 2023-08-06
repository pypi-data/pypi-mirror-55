# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 15:39
# @E-Mail  : aberstone.hk@gmail.com
# @File    : types.py
# @Software: PyCharm
from typing import Union, Sequence, AnyStr, TypeVar

from scrapy import Spider, Request
from scrapy.crawler import Crawler
from scrapy_redis.spiders import RedisSpider

_Proxies = Union[Sequence[AnyStr], AnyStr]
_Crawler = Crawler
_Spider = Union[Spider, RedisSpider]
_Request = Request
