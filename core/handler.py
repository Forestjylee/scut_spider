# -*- coding: utf-8 -*-
"""
调度器
@file: handler.py
@time: 2019/4/18 15:17
Created by Junyi
"""
import configparser
from requests import get
from multiprocessing import Pool
from core.spider import crawl
from utils.log_helper import get_logger
from pipeline.redis_pipeline import RedisPipeline
from pipeline.output_pipeline import OutputPipeline


class Handler(object):
    """总调度类"""

    def __init__(self):
        self._init_config_parser()
        self.start_url = self._config_parser.get("url", "start_url")
        self.limit_domain = self._config_parser.get("url", "limit_domain")
        self.redis_host = self._config_parser.get("redis", "host")
        self.redis_port = self._config_parser.getint("redis", "port")
        self.redis_uncrawled_name = self._config_parser.get("redis", "uncrawled_set_name")
        self.redis_crawled_name = self._config_parser.get("redis", "crawled_set_name")
        self.is_multiprocess = self._config_parser.getboolean("multiprocess", "switch")
        self.process_num = self._config_parser.getint("multiprocess", "process_num")
        self.log_file_name = self._config_parser.get("log", "file_name")
        self.is_log_to_console = self._config_parser.getboolean("log", "to_console")
        self.is_log_to_file = self._config_parser.getboolean("log", "to_file")

    def _run(self) -> None:
        """
        1、获取redis操作对象
        2、获取output管道操作对象
        3、判断redis队列中是否有url
        4、从redis中取出一个url
        5、执行爬取函数，返回网站信息
        6、将信息输出到output管道
        7、讲新的urls加入到redis队列
        8、更新日志
        :return: None
        """
        rp = self._get_redis_pipeline()
        op = self._get_output_pipeline()
        logger = self._get_logger()
        while 1:
            if rp.is_queue_empty():
                break
            try:
                url = rp.get_one_url()
                info = crawl(url=url, limit_domain=self.limit_domain)
                op.save(data=info)
                rp.add_urls_in_set(info['links'])
                logger.info(f"{url} has been crawled successfully.")
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(repr(e))

    def start(self) -> None:
        """
        主函数入口
        判断是否进行多进程爬取
        :return: None
        """
        self.check()
        if self.is_multiprocess:
            pool = Pool(processes=self.process_num)
            for _ in range(self.process_num):
                pool.apply_async(self._run)
            pool.close()
            pool.join()
        else:
            self._run()

    def check(self) -> None:
        """
        运行前检查网络连通情况
        若是第一次运行则从起始url开始爬取
        :return: None
        """
        try:
            get('http://www.baidu.com')
        except Exception as e:
            print(f"当前网络环境异常!\nError message:{repr(e)}")
            exit(-1)
        rp = self._get_redis_pipeline()
        op = self._get_output_pipeline()
        logger = self._get_logger()
        if not rp.is_exists():
            info = crawl(url=self.start_url, limit_domain=self.limit_domain)
            op.save(data=info)
            rp.add_urls_in_set(info['links'])
            logger.info(f"{self.start_url} has been crawled successfully.")

    def _get_redis_pipeline(self) -> RedisPipeline:
        """获取操作redis数据库的对象"""
        return RedisPipeline(
            host=self.redis_host,
            port=self.redis_port,
            name=self.redis_uncrawled_name,
            crawled_name=self.redis_crawled_name,
        )

    def _get_logger(self):
        """
        获取日志输出对象
        :return:
        """
        return get_logger(
            to_console=self.is_log_to_console,
            to_file=self.is_log_to_file,
            filename=self.log_file_name,
        )

    def _get_output_pipeline(self) -> OutputPipeline:
        """获取输出管道操作对象"""
        return OutputPipeline(self._config_parser)

    def _init_config_parser(self) -> None:
        """
        初始化配置解析器
        :return: 配置解析器
        """
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read("config.ini", encoding="utf-8")
