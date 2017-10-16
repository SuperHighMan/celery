#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : JDSpider.py
# @Author: Hui
# @Date  : 2017/10/16
# @Desc  :

import requests
import time
import re
import jieba.analyse
from  wordcloud  import  WordCloud
import  matplotlib.pyplot  as  plt

headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

url1 = 'https://club.jd.com/comment/productPageComments.action?' \
      'callback=fetchJSON_comment98vv110230&productId=1127466&score=0&sortType=5&page='
url2 = '&pageSize=10&isShadowSku=0&rid=0&fold=1'

def getComment():
    result = open('JD_spider.txt','w+')
    for i in range(100):
        url = url1 + str(i) + url2
        print(url)
        response = requests.get(url, headers)
        response.encoding = 'gbk'
        content = response.text
        time.sleep(0.3)
        result.write(content)
        result.write('\n')
    result.close()

def commentAnalyze():
    #获取评论
    pattern = '"content":(.*?),'
    result = open('JD_spider.txt').read()
    content = re.findall(pattern, result)
    content_list = []
    for i in content:
        if not 'img' in i:
            content_list.append(i)

    contents = ''.join(content_list)
    contents_rank = jieba.analyse.extract_tags(contents, topK=30, withWeight=True)
    print(contents_rank)

    key_words = dict()
    for i in contents_rank:
        key_words[i[0]] = i[1]
    print(key_words)
    wc = WordCloud(font_path='./fonts/simhei.ttf', background_color='White',
                   max_words=50)
    wc.generate_from_frequencies(key_words)
    plt.imshow(wc)
    plt.axis("on")
    plt.show()

if __name__ == '__main__':
    #getComment()
    commentAnalyze()
    print('hello')