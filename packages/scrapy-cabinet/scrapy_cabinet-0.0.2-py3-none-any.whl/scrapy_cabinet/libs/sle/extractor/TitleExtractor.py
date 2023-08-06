# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 17:47
# @E-Mail  : aberstone.hk@gmail.com
# @File    : TitleExtractor.py
# @Software: PyCharm
import re
from typing import Union, Dict, List, AnyStr

from jsonpath import jsonpath
from lxml.html import HtmlElement
from scrapy_cabinet.utils import LOGGER

from scrapy_cabinet.libs.defaults import TITLE_PATTERN_XPATH, TITLE_JSON_KEYS
from scrapy_cabinet.libs.utils import pre_parse, one_layer_dict


class TitleExtractor(object):
    def __init__(self, title_key: str = ""):
        self.title_xpath_pattern = TITLE_PATTERN_XPATH
        self.title_key = title_key

    def _json_extractor(self, json_dict: Union[Dict, List]):
        text = ""
        if self.title_key:
            text = "".join(jsonpath(json_dict, self.title_key))
            LOGGER.info(
                "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                    "title_args",
                    self.title_key,
                    text
                )
            )
        else:
            tmp = one_layer_dict(json_dict)
            keys_default_list = [TITLE_JSON_KEYS for _ in range(len(tmp))]
            for i in filter(
                    lambda x: any([i in x[0].lower() for i in x[1]]) and tmp[x[0]],
                    zip(tmp.keys(), keys_default_list)
            ):
                text = tmp[i[0]]
                break
            if text:
                LOGGER.info(
                    "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format(
                        "title_default",
                        "title in dict.keys",
                        text
                    )
                )
        return text

    def _xpath_extractor(self, element: HtmlElement):
        if self.title_key:
            text = "".join(element.xpath(self.title_key))
            # LOGGER
            LOGGER.info("PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format("title_args", self.title_key, text))
            return text
        for xpath_str in self.title_xpath_pattern:
            text = "".join(element.xpath(xpath_str))
            if text:
                # LOGGER
                LOGGER.info(
                    "PATTERN_TYPE: {} || PATTERN: {} || RESULT: {}".format("title_default", xpath_str, text))
                return text
        _ = ''.join(element.xpath('.//text()'))

    def extractor(self, source: Union[Dict, List, HtmlElement, AnyStr]) -> str:
        if isinstance(source, (HtmlElement, str)):
            source = pre_parse(source)
            return self._xpath_extractor(source)
        return self._json_extractor(source)
