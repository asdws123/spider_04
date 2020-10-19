"""
多线程抓取百度指定关键字的所有图片
"""
import requests
from threading import Thread, Lock
from queue import Queue
from urllib import parse
import os
from fake_useragent import UserAgent

class BaiduImageSpider:
    def __init__(self):
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7894352681936632113&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30&gsm=1e&1603077672039='
        self.q = Queue()
        self.lock = Lock()
        # 用户输入,创建对应的目录结构
        self.word = input('请输入关键字:')
        self.directory = './images/{}/'.format(self.word)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        # url编码
        self.params = parse.quote(self.word)

    def get_html(self, url):
        """请求功能函数"""
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url, headers=headers).json()

        return html

    def get_total(self):
        """获取图片总数量"""
        total_url = self.url.format(self.params, self.params, 30)
        total_html = self.get_html(url=total_url)
        # 获取总数
        return total_html['displayNum']

    def url_in_q(self):
        """url地址入队列"""
        total = self.get_total()
        for pn in range(30, total + 30, 30):
            page_url = self.url.format(self.params, self.params, pn)
            # 入队列
            self.q.put(page_url)

    def save_image(self, image_url):
        """保存1张图片到本地文件"""
        headers = {'User-Agent':UserAgent().random}
        image_html = requests.get(url=image_url, headers=headers).content
        # 处理文件名,写入到本地
        # filename: ./images/赵丽颖/xxx.jpg
        filename = self.directory + image_url[-30:]
        with open(filename, 'wb') as f:
            f.write(image_html)
        # 终端加个提示
        print(filename,'下载成功')

    def get_one_page_images(self, page_url):
        """获取一页中所有的30张图片"""
        # page_html:提取30张图片链接
        page_html = self.get_html(url=page_url)
        # [:-1]: 处理掉最后一个空字典
        for one_image_dict in page_html['data'][:-1]:
            # 图片链接
            image_url = one_image_dict['hoverURL']
            # 条件判断: 有部分数据无 hoveURL
            if image_url:
                # 保存1张图片到本地文件
                self.save_image(image_url)

    def parse_html(self):
        """线程事件函数"""
        while True:
            # 加锁
            self.lock.acquire()
            if not self.q.empty():
                page_url = self.q.get()
                # 释放锁
                self.lock.release()
                # 获取page_url中的30张图片的函数
                self.get_one_page_images(page_url)
            else:
                # 释放锁
                self.lock.release()
                break

    def run(self):
        """程序入口函数"""
        # 先让URL地址入队列
        self.url_in_q()
        # 创建多线程
        t_list = []
        for i in range(3):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()

if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.run()





















