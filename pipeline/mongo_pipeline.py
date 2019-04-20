# -*- coding: utf-8 -*-
"""
与MongoDB数据库的交互
@file: mongo_pipeline.py
@time: 2019/04/18 19:42
Created by Junyi.
"""
import pymongo


class MongoPipeline(object):

    def __init__(self, config_parser):
        """
        :param config_parser: 配置解析器
        """
        self.db_name = config_parser.get("mongoDB", "database_name")
        self.collection_name = config_parser.get("mongoDB", "collection_name")
        self._client = pymongo.MongoClient(
            host=config_parser.get("mongoDB", "host"),
            port=config_parser.getint("mongoDB", "port"),
        )

    def save_data(self, data: dict) -> None:
        """
        将爬取到的html数据存储到MongoDB中
        :param data: 需要存储的数据
        :return: None
        """
        self._client[self.db_name][self.collection_name].insert_one(data)
