# -*- coding: utf-8 -*-
"""
与MongoDB数据库的交互
@file: mongo_pipeline.py
@time: 2019/04/18 19:42
Created by Junyi.
"""
import pymongo
from settings import (MONGODB_HOST, MONGODB_PORT,
                      MONGODB_DATABASE_NAME, MONGODB_COLLECTION_NAME)


class MongoPipeline(object):

    def __init__(self):
        self.db_name = MONGODB_DATABASE_NAME
        self.collection_name = MONGODB_COLLECTION_NAME
        self._client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)

    def save_data(self, data: dict) -> None:
        """
        将爬取到的html数据存储到MongoDB中
        :param data: 需要存储的数据
        :return: None
        """
        self._client[self.db_name][self.collection_name].insert_one(data)
