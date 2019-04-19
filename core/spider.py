# -*- coding: utf-8 -*-
"""
爬虫主体
@file: spider.py
@time: 2019/4/8 17:22
Created by Junyi
"""
from requests_html import HTMLSession, HTMLResponse


def get_response(url: str) -> HTMLResponse:
    """
    向指定url发起HTTP GET请求
    返回Response
    :param url: 目标url
    :return: url响应
    """
    session = HTMLSession()
    return session.get(url)


def parse_response(response: HTMLResponse, source_url: str, limit_domain: str) -> dict:
    """
    解析url的响应
    :param response: url的响应
    :param source_url: response的来源url
    :param limit_domain: 限制保留的域名字符串
    :return: 需要获取的信息 {
        'source': 此响应来自哪个url,
        'raw_text': 初步提取出的文本信息,
        'links': 此网站指向外部的urls(只保留url中含有'scut.edu.cn'的)
    }
    """
    info = {
        'source': source_url,
        'raw_text': response.html.text,
        'links': [
            url for url in response.html.absolute_links if limit_domain in url and url != source_url
        ],
    }
    return info


def crawl(url: str, limit_domain: str) -> dict:
    """
    向指定url发起HTTP GET请求
    返回需要的信息字典
    :param url: 目标url
    :param limit_domain: 限制保留的域名字符串
    :return: 需要获取的信息 {
        'source': 此响应来自哪个url,
        'raw_text': 初步提取出的文本信息,
        'links': 此网站指向外部的urls,
    }
    """
    response = get_response(url)
    info = parse_response(response, url, limit_domain)
    return info
