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
            name: str='Default'
    ):
        """
        :param host: redis数据所在的ip地址
        :param port: redis数据库所在的端口
        :param name: 数据表名称
        """
        self.host = host
        self.port = port
        self.name = name
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

    def get_one_item(self) -> str:
        """
        取出redis集合中的随机一个元素
        :return: item | None(队列为空时)
        """
        return self._redis_obj.spop(self.name)

    def add_items_in_set(self, items) -> int:
        """
        将多个item加入redis集合中
        :param items: 需要新增的元素
        :return: 成功添加进入集合中的元素的个数
        """
        return self._redis_obj.sadd(self.name, *items)

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
