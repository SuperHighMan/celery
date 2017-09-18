#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests
import re
import time

def News():
    url = "http://news.163.com/rank/"
    response = requests.get(url)
    content = requests.get(url).content
    print("response headers:", response.headers)
    print("content:", content)

def GetSpider(page):
    url = "https://www.qiushibaike.com/text/page/1"
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    for i in range(1, page+1):
        #实现翻页
        url = re.sub('page/\d+', 'page/%d'%i, url, re.S)
        print(url)
        #发送请求，获得返回的信息
        response = requests.get(url, headers)
        content = response.content.decode('utf-8')
        #处理获取的网页内容
        items = re.findall('<div class="content">(.*?)</div>', content, re.S)
        print(items)
        for j in range(0, len(items)):
            file = open('qiushi.txt', 'a')
            file.write(str(j+1) + ':')
            file.write(items[j])
            file.write('\n')
        #设置延时
        time.sleep(5)


def test():
    import urllib.request

    # 定义保存函数
    def saveFile(data):
        path = "douban.html"
        f = open(path, 'wb')
        f.write(data)
        f.close()

        # 网址

    url = "https://www.qiushibaike.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)

    res = urllib.request.urlopen(req)

    data = res.read()

    # 也可以把爬取的内容保存到文件中
    saveFile(data)

    data = data.decode('utf-8')
    # 打印抓取的内容
    print(data)

    # 打印爬取网页的各类信息
    print(type(res))
    print(res.geturl())
    print(res.info())
    print(res.getcode())

if __name__ == '__main__':
    print('爬虫开始')
    GetSpider(30)
    print('爬虫程序结束')
    #test()

