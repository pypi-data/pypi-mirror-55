# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 16:57
# @E-Mail  : aberstone.hk@gmail.com
# @File    : __init__.py.py
# @Software: PyCharm
import json
import re
from typing import Union, AnyStr
from lxml.html import HtmlElement
from scrapy_cabinet.utils import LOGGER

from scrapy_cabinet.libs.sle.extractor import TimeExtractor, ListExtractor, URLExtractor, TitleExtractor


class SmartListInfoExtractor(object):

    def __init__(self, list_key: str = "", time_key: str = "", title_key: str = "", url_key: str = ""):
        self.list_extractor = ListExtractor(list_key)
        self.time_extractor = TimeExtractor(time_key)
        self.url_extractor = URLExtractor(url_key)
        self.title_extractor = TitleExtractor(title_key)

    def extract(self, html: Union[AnyStr, HtmlElement]):
        result = []
        list = self.list_extractor.extractor(html)

        for index, i in enumerate(list):
            LOGGER.warning(index)
            result.append({
                "url": self.url_extractor.extractor(i),
                "title": self.title_extractor.extractor(i),
                "time": self.time_extractor.extractor(i)
            })

        return result


if __name__ == '__main__':
    with open("extractor/resutl", "r") as f:
        r = f.read()
    # re_compile = re.compile(r"allData = (\{.*?\});", re.DOTALL)
    # content = json.loads(re_compile.findall(r)[0])
    # extractor = SmartListInfoExtractor(url_key='((finance|news|tech)\.ifeng\.com/c/[0-9a-zA-Z]+)')
    extractor = SmartListInfoExtractor()

    # print(content)
    result = extractor.extract(r)
    LOGGER.warning(result)
