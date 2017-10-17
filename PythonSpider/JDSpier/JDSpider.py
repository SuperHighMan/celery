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
from matplotlib.pyplot import savefig

headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

url1 = 'https://club.jd.com/comment/productPageComments.action?' \
      'callback=fetchJSON_comment98vv110230&productId=1127466&score=0&sortType=5&page='
url2 = '&pageSize=10&isShadowSku=0&rid=0&fold=1'

tburl1 = 'https://rate.tmall.com/list_detail_rate.htm?itemId=538705099322&' \
        'spuId=382711454&sellerId=2616970884&order=3&' \
        'currentPage='
tburl2 ='&append=0&content=1&tagId=&posi=&' \
        'picture=&ua=098%23E1hvtvvavfGvUvCkvvvvvjiPP2Lh6jYjPFMO6j1VPmPwAjimnL' \
        'LZAj1bRFFOgjrnRphvCvvvvvmCvpvWzCAhO7LNznsw2bY4dphvmpvUvOPDtpvmwT6Cvvyvmhv' \
        'h7H9vkBmrvpvEvvpw9AOevhZEdphvmpvhUUR%2Bdv2ZI9wCvvNwzHi4zMC3dphvmpvUyQpP2Qmv' \
        'JUhCvvswjjn9gnMwznsY4DIPvpvhvv2MMTyCvv9vvUmSXvS03OyCvvOUvvVvaZ8tvpvIvvvvbhCvvv' \
        'vvvUUdphvU89vv9krvpvQvvvmm86CvmU%2BvvUUdphvU89yCvhQW%2FKWvCAJxfwCl5dUf8z7%2BkWeARmGn' \
        '%2B8c6tCKfax5XS47BhC3qVUcnDOmOjjIUDajxALwpEcqZaNoxdX9aWg033we3rABCCaV9D40fvphvC9vhvv' \
        'Cvp2yCvvpvvvvviQhvCvvv9U8jvpvhvvpvv86CvvyvmEh2X7ZvjHwtvpvhvvvvv86CvvyvmUTmq%2FGvRnWt' \
        'vpvhvvvvv86CvvyvmV82BhpvDORrvpvZbvA1vYFOvP6l84GuUZWE3wyErsQtvpvhvvvvvvwCvvNwzHi4zQQ' \
        'FRphvCvvvvvmrvpvEvvL19Tuuvmd89phvHnQwxVuUzYswzbjl7%2FYSMvfw9HuC&needFold=0&_ksTS=1508' \
        '144868405_2934&callback=jsonp2935'

def getComment(file, url1, url2):
    result = open(file,'w+')
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

def commentAnalyze(file):
    #获取评论
    pattern = '"reply":(.*?),'
    result = open(file).read()
    content = re.findall(pattern, result)
    content_list = []
    for i in content:
        if not 'img' in i:
            content_list.append(i)
    print("总计评论：%d个" %(len(content_list)))

    #jieba分词
    contents = ''.join(content_list)
    contents_rank = jieba.analyse.extract_tags(contents, topK=30, withWeight=True)
    print(contents_rank)

    # WordCloud可视化
    key_words = dict()
    for i in contents_rank:
        key_words[i[0]] = i[1]
        print('%s : %f' %(i[0], i[1]) )

    wc = WordCloud(font_path='./fonts/simhei.ttf', background_color='White',
                   max_words=50)
    wc.generate_from_frequencies(key_words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    #savefig('r.jpg')

def QQAnalyze():
    pattern = 'msg=(.*?),'
    f = open('QQ').read()
    content = re.findall(pattern, f)
    content_list = []
    for i in content:
        if not 'CQ:at' in i:
            content_list.append(i)

    #jieba分词
    contents = ''.join(content_list)
    contents_rank = jieba.analyse.extract_tags(contents, topK=30, withWeight=True)
    print(contents_rank)

    # WordCloud可视化
    key_words = dict()
    for i in contents_rank:
        key_words[i[0]] = i[1]
    wc = WordCloud(font_path='./fonts/simhei.ttf', background_color='White',
                   max_words=50)
    wc.generate_from_frequencies(key_words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    file = 'ip6s.txt'
    #getComment(file=file, url1=tburl1, url2=tburl2)
    commentAnalyze(file=file)
    #QQAnalyze()
    print('hello')