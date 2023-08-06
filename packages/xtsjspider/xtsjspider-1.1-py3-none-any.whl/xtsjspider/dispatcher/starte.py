import queue

from xtsjspider.abnormal import abnorm
from xtsjspider.downloader.HTTP import HttpRequest
from xtsjspider.model.modeler import Model

URL_MANAGER = queue.Queue(999999)


# 开始下载器类
class RunSpider(object):
    start_url = None

    def __init__(self):
        if self.start_url is not None:
            URL_MANAGER.put(self.start_url)
            urls = self.insert_url()  # 添加爬虫url
            if not isinstance(urls, list):
                raise abnorm.InsertUrlNotList

            for url in urls:
                URL_MANAGER.put(url)

            self.scheduling()  # 开始调度
        else:
            raise abnorm.StartUrlNotNone  # 抛出异常

    def start(self, response):
        '''
        该方法给用户重定义
        :param response: HttpResponse对象
        :return: 返回模型类， 或者HttpRequest类
        '''
        pass

    def scheduling(self):
        while not URL_MANAGER.empty():  # URL没有空间了结束
            response = HttpRequest(URL_MANAGER.get()).get()
            data = self.start(response)  # 调用用户方法

            # 根据用户方法进行调用,并且释放空间

            if isinstance(data, Model):  # 调用保存方法
                self.open_data(data.data)
                del data

            elif isinstance(data, HttpRequest):  # 下载器方法
                URL_MANAGER.put(data.url)
                print(data)
                del data

    def open_data(self, data, *args):
        '''

        :param args: 用户自定义保留爬虫方法。
        :return: None
        '''
        pass

    def insert_url(self):
        '''
        用户定义
        :return: 返回一个list , 用于添加url
        '''
        return []
