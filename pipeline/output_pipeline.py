# -*- coding: utf-8 -*-
"""
爬取信息输出管道
@file: output_pipeline.py
@time: 2019/4/18 15:50
Created by Junyi
"""
from pprint import pprint
from pipeline.mongo_pipeline import MongoPipeline
from settings import USE_MONGO_PIPELINE


class OutputPipeline(object):
    """
    输出管道实现类
    注意：
    由于可能用于多进程环境下执行，
    若需要保存到文件中则需使用文件锁保证同步，
    推荐保存在数据库中
    """
    def __init__(self):
        self.op = MongoPipeline() if USE_MONGO_PIPELINE else PrintPipeline()

    def save(self, data: dict):
        """
        将信息保存到指定位置
        :param data: 数据信息
        :return:
        """
        self.op.save_data(data)


class PrintPipeline(object):

    def __init__(self):
        pass

    @staticmethod
    def save_data(data: dict) -> None:
        """
        将信息输出到控制台
        :param data: 信息
        :return: None
        """
        pprint(data)
