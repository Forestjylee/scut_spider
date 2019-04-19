# -*- coding: utf-8 -*-
"""
redis交互类
@file: redis_pipeline.py
@time: 2019/4/18 14:59
Created by Junyi
"""
import redis


class RedisPipeline(object):
    """
    与redis数据库交互的接口
    windows版本的redis数据库下载地址:https://github.com/MSOpenTech/redis/releases
    """
    def __init__(
            self,
            host: str='localhost',
            port: str='6379',
            name: str='Default',
            crawled_name: str='Crawled',
    ):
        """
        :param host: redis数据所在的ip地址
        :param port: redis数据库所在的端口
        :param name: 存储待请求url集合名称
        :param crawled_name: 存储被请求过url集合的名称
        """
        self.host = host
        self.port = port
        self.name = name
        self.crawled_name = crawled_name
        self._redis_obj = self.__get_redis_obj()

    def __get_redis_obj(self) -> redis.Redis:
        """
        获取redis对象
        :return: 操作redis数据库的对象
        """
        redis_obj = redis.Redis(host=self.host, port=int(self.port))
        return redis_obj

    def get_length(self):
        """
        获取当前集合中元素的个数
        :return: 元素的个数
        """
        return self._redis_obj.scard(self.name)

    def get_one_url(self) -> str:
        """
        取出redis集合中的随机一个url
        将改url加入到已爬取几集合中
        :return: url | None(队列为空时)
        """
        url = self._redis_obj.spop(self.name)
        self._redis_obj.sadd(self.crawled_name, url)
        return url

    def add_urls_in_set(self, urls: list) -> None:
        """
        将多个url加入redis集合中
        剔除被请求过的url
        :param urls: 需要新增的元素
        :return: None
        """
        for url in urls:
            if not self._redis_obj.sismember(self.crawled_name, url):
                self._redis_obj.sadd(self.name, url)

    def is_queue_empty(self) -> bool:
        """s
        判断redis队列是否为空
        :return: True | False
        """
        if self.get_length():
            return False
        else:
            return True

    def is_exists(self) -> bool:
        """
        判断集合是否存在
        :return: True | False
        """
        nums = self._redis_obj.exists(self.name)
        return True if nums else False
