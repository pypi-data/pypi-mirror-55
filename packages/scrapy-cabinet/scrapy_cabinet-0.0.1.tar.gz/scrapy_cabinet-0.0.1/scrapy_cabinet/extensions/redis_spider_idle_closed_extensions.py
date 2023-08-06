# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 15:35
# @E-Mail  : aberstone.hk@gmail.com
# @File    : redis_spider_idle_closed_extensions.py
# @Software: PyCharm
from scrapy import signals
from scrapy.exceptions import NotConfigured

from scrapy_cabinet.types import _Crawler,_Spider


class RedisSpiderIdleClosedExtensions(object):
    """A base DownloaderMiddleware to set proxy to Scrapy request.

    To use this Middleware, Project should set proxy_url or proxy_pool in settings.py.
    When use PROXY_URL, PROXY_TYPE should be set at the same time.
        PROXY_TYPE == 1 or PROXY_TYPE == 0.

    Attributes:
        proxies : _Proxies : A _Proxies type to store proxy_url.
        is_init : bool     : A bool value to check the proxies is set successfully

    Methods:
        get_proxies  | Args: NaN | A method to get proxy_url, when use proxy_url and proxy_type == 1
                                   this method can not be implemented.

    """

    def __init__(self, idle_num: int, crawler: _Crawler):
        self.crawler = crawler
        self.idle_num = idle_num
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler: _Crawler) -> object:
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured
        if not 'redis_key' in crawler.spidercls.__dict__.keys():
            raise NotConfigured("ONLY SUPPORT REDISSPIDER")

        idle_num = crawler.settings.getint("IDLE_NUMBER", 120)
        ext = cls(idle_num, crawler)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        return ext

    def spider_opened(self, spider:_Spider):
        spider.logger.info("opened spider {}, Allow waiting time:{} second".format(spider.name, self.idle_num * 5))

    def spider_closed(self, spider:_Spider):
        spider.logger.info("closed spider {}, Waiting time exceeded {} second".format(spider.name, self.idle_num * 5))

    def spider_idle(self, spider:_Spider):
        # 程序启动的时候会调用这个方法一次，之后每隔5秒再请求一次
        # 当持续10min都没有spider.redis_key，就关闭爬虫
        # 判断是否存在 redis_key
        if not spider.server.exists(spider.redis_key):
            self.idle_count += 1
        else:
            self.idle_count = 0

        if self.idle_count > self.idle_num:
            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'Waiting time exceeded')
