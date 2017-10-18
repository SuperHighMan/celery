#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : douban.py
# @Author: Hui
# @Date  : 2017/10/17
# @Desc  :

'''
#2017.10.18
#豆瓣登录 https://www.douban.com
#现阶段需要人工输入验证码进行登录

#下一步的想法是自动识别验证码进行登录
'''

import requests
from bs4 import BeautifulSoup
from http import cookiejar
from urllib.request import urlretrieve
import re
import os

headers = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, sdch, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Connection":"keep-alive",
    "Host":"www.douban.com",
    'Referer': 'https://www.douban.com/',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"
}

login_url = 'https://accounts.douban.com/login'

#使用cookie信息
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print('Cookie can not be loaded')

#获取验证码
def get_captcha():
    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    img_src = soup.find('img', {'id':'captcha_image'}).get('src')
    print(img_src)
    urlretrieve(img_src, 'douban.jpg')
    captcha = input('please input the captcha:')
    os.remove('douban.jpg')
    captcha_id = soup.find('input', {'name':'captcha-id'}).get('value')
    return captcha, captcha_id

#判断是否需要验证码
def needCaptcha():
    response = session.get(login_url, headers=headers)
    pattern = r'captcha-id'
    result = re.findall(pattern, response.text)
    if len(result) == 0:
        return False
    else:
        return True

#登录
def login(account, password):
    captcha = ''
    captcha_id = ''
    if needCaptcha():
        captcha, captcha_id = get_captcha()
    data = {
    'source': 'index_nav',
    'redir': 'https://www.douban.com/',
    'form_email': account,
    'form_password': password,
    'remember': 'on',          #此参数需要设置，不然不能使用cookie登录
    'captcha-solution': captcha,
    'captcha-id': captcha_id
    #'login': '登录'
    }
    response = session.post(login_url, data=data, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    messages  = soup.findAll('div', attrs={'class': 'title'})
    for i in messages:
        print(i.find('a').get_text())
    session.cookies.save()

#判断是否已经登录
def isLogin():
    response = session.get('https://www.douban.com/accounts/',
                           headers=headers, allow_redirects=False)
    print(response.status_code)
    if response.status_code == 200:
        return True
    else:
        return False

if __name__ == '__main__':
    if isLogin():
        print('已经登录')
    else:
        account = input('请输入你的帐号:')
        password = input('请输入你的密码:')
        login(account, password)
