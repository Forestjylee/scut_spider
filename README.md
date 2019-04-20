# scut_spider

🍻爬取SCUT相关网页🍻

[TOC]

## 1.环境搭建

### 1.1.Python环境

&emsp;&emsp;scut_spider依赖的Python解释器版本为3.7，使用pipenv可以轻松完成虚拟环境的创建。首先确保本地主机已安装pipenv

```shell
>>> pip install -U pipenv
```

&emsp;&emsp;然后开始进入scut_spider目录进行虚拟环境的创建：

```shell
>>> cd scut_spider
>>> pipenv install --skip-lock
```

&emsp;&emsp;（--skip-lock的作用是跳过pipenv 的lock操作，这一步往往需要较长时间）

&emsp;&emsp;接下来只需要等待虚拟环境安装成功即可。需要注意的是，pipenv创建虚拟环境使用的是本地的Python3.7解释器，若本地没有3.7版本的Python解释器就会报错。若不想再本地安装Python3.7解释器，可以打开Pipdile文件，将最后的python_version修改为适合自己主机的Python版本(不建议这样做)。

&emsp;&emsp;scut_spider的包依赖如下所示：

```shell
>>> pipenv graph
pymongo==3.7.2
redis==3.2.1
requests-html==0.10.0
  - bs4 [required: Any, installed: 0.0.1]
    - beautifulsoup4 [required: Any, installed: 4.7.1]
      - soupsieve [required: >=1.2, installed: 1.9.1]
  - fake-useragent [required: Any, installed: 0.1.11]
  - parse [required: Any, installed: 1.12.0]
  - pyppeteer [required: >=0.0.14, installed: 0.0.25]
    - appdirs [required: Any, installed: 1.4.3]
    - pyee [required: Any, installed: 6.0.0]
    - tqdm [required: Any, installed: 4.31.1]
    - urllib3 [required: Any, installed: 1.24.2]
    - websockets [required: Any, installed: 7.0]
  - pyquery [required: Any, installed: 1.4.0]
    - cssselect [required: >0.7.9, installed: 1.0.3]
    - lxml [required: >=2.1, installed: 4.3.3]
  - requests [required: Any, installed: 2.21.0]
    - certifi [required: >=2017.4.17, installed: 2019.3.9]
    - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
    - idna [required: >=2.5,<2.9, installed: 2.8]
    - urllib3 [required: >=1.21.1,<1.25, installed: 1.24.2]
  - w3lib [required: Any, installed: 1.20.0]
    - six [required: >=1.4.1, installed: 1.12.0]
```



### 1.2.MongoDB数据库

MongoDB数据库的安装网上有许多教程，这里提供一个：

http://www.runoob.com/mongodb/mongodb-window-install.html

推荐一个MongoDB的可视化工具(Robo 3T)：

https://robomongo.org/



### 1.3.Redis数据库

Redis数据库官方不提供Windows版本，这里提供一个微软官方发布的版本：

https://github.com/MSOpenTech/redis/releases

推荐一个Redis可视化工具：

https://github.com/uglide/RedisDesktopManager/releases/download/0.9.3/redis-desktop-manager-0.9.3.817.exe



## 2.运行爬虫

### 2.1.配置爬虫

&emsp;&emsp;scut_spider的配置文件config.ini存放在根目录下，默认配置为：

```ini
[url]
start_url = https://www.scut.edu.cn/new/    # 起始url
limit_domain = scut.edu.cn                  # 只爬取带有此字符串的url

[redis]
host = localhost                            # redis服务器ip地址
port = 6379                                 # redis端口号
crawled_set_name = Crawled                  # 存放已爬取url的redis集合名称
uncrawled_set_name = Uncrawled              # 存放未爬取url的redis集合名称

[mongoDB]
switch = True                               # 是否启用MongoDB保存爬取到的数据
host = localhost                            # MongoDB服务器ip地址
port = 27017                                # MongoDB端口号
database_name = scut_spider                 # 存放爬取数据的MongoDB数据库名称
collection_name = collection1               # 存放爬取数据的MongoDB数据表名称

[multiprocess]
switch = True                               # 是否启用多进程模式
process_num = 7                             # 并行的进程数(并非越大越好)

[log]
file_name = scut_spider                     # 日志文件名称
to_console = True                           # 是否将日志信息输出到控制台
to_file = True                              # 是否将日志信息保存至文件
```



### 2.2.重构pipeline

&emsp;&emsp;目前scut_spider只有两种output_pipeline，若想将数据保存到自己想要的地方，可以重构scut_spider/pipeline/output_pipeline中的OutputPipeline类的save函数。&emsp;&emsp;OutputPipeline类：

```python
class OutputPipeline(object):
    """
    输出管道实现类
    注意：
    由于可能用于多进程环境下执行，
    若需要保存到文件中则需使用文件锁保证同步，
    推荐保存在数据库中
    """
    def __init__(self, config_parser):
        """
        :param config_parser: 配置解析器
        """
        self.op = MongoPipeline(config_parser) \
            if config_parser.getboolean("mongoDB", "switch") else PrintPipeline()

    def save(self, data: dict):
        """
        将信息保存到指定位置
        :param data: 数据信息
        :return:
        """
        self.op.save_data(data)
```



### 2.3.保存的数据格式

&emsp;&emsp;以字典的形式保存爬取的信息，格式如下：

```python
info = {
    'source': source_url,
    'raw_text': response.html.text,
    'links': [
        url for url in response.html.absolute_links if limit_domain in url
    ],
}
```

&emsp;&emsp;使用时可以根据需要重构这部分代码。(scut_spider/core/spider.py)



## 3.其他

&emsp;&emsp;scut_spider不止是针对某个网站的爬虫，理论上它可以爬取任意的网站，只需要修改config.ini中的配置即可。

```python
@Author: Junyi
@Time: 2019/4/19 19:17
```

