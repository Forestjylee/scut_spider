# -*- coding: utf-8 -*-
"""
配置文件
@file: settings.py
@time: 2019/4/18 15:23
Created by Junyi
"""


# 爬虫起始地址
START_URL = 'https://www.scut.edu.cn/new/'


# 爬取过程中保留的网址
LIMIT_DOMAIN = 'scut.edu.cn'


# redis数据库所在ip地址
REDIS_HOST = 'localhost'


# redis数据库所在端口(通常为6379)
REDIS_PORT = 6379


# 存放待请求url的redis集合名称
REDIS_SET_NAME = 'Default'


# 已请求过的url集合名称
CRAWLED_SET_NAME = 'Crawled'


# 是否启用多进程模式(True|False)
MULTIPROCESS_SWITCH = True


# 并行的进程数(并非越大越好，根据实际情况选择)
PROCESS_NUM = 7


# 日志文件名
LOG_FILE_NAME = 'scut_spider'


##############################################


# 是否保存到MongoDB(True|False)
USE_MONGO_PIPELINE = False


# mongoDB数据库所在ip地址
MONGODB_HOST = 'localhost'


# mongoDB数据库所在端口号
MONGODB_PORT = 27017


# mongoDB数据库名称
MONGODB_DATABASE_NAME = 'scut_data'


# mongoDB数据库表名称
MONGODB_COLLECTION_NAME = 'collection1'
