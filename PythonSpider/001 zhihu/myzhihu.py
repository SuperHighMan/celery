#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : myzhihu.py
# @Author: Hui
# @Date  : 2017/10/17
# @Desc  :

'''
#2017.10.17测试发现
#带有lang=cn的链接是知乎现在新的验证码方式，采用倒立的汉字captcha_url_new
#可以采用原来的图片验证方式，目前仍然能够登陆知乎，验证码获得方式为captcha_url_pic
captcha_url_new = 'https://www.zhihu.com/captcha.gif?r=1508202068105&type=login&lang=cn'
captcha_url_pic = 'https://www.zhihu.com/captcha.gif?r=1508202068105&type=login'
phone_url = 'https://www.zhihu.com/login/phone_num'
'''

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib import parse

#使用cookie登陆
from http import cookiejar
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except :
    print('load cookies failed')

# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, sdch, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Connection":"keep-alive",
    "Host":"www.zhihu.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"
}

#获取xsrf
def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=headers)
    #使用bs获取_xsrf的值
    soup = BeautifulSoup(response.content, 'lxml')
    xsrf = soup.find('input', attrs={'name':'_xsrf'}).get('value')
    #使用正则表达式获取_xsrf的值
    #pattern = r'name="_xsrf" value="(.*?)"'
    #xsrf = re.findall(pattern, response.text)
    return xsrf

#处理图片验证码
def get_picture():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
    print(captcha_url)
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    console = input("验证码：")
    return console

#处理倒立的汉字的验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=cn'
    print(captcha_url)
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    console = input("验证码：")
    captcha = generate_captcha(console)
    #print(captcha)
    return captcha


#根据用户的判断构造验证码的参数值
#构造类似于如下的参数：
#captcha = {"img_size":[200,44],"input_points":[[67,28.6094],[28,29.6094]]}
def generate_captcha(str):
    pointMap = {
        '1': '[17,10.60938]',
        '2': '[43,24.6094]',
        '3': '[75,22.6094]',
        '4': '[93,11.60938]',
        '5': '[121,28.6094]',
        '6': '[143,29.6094]',
        '7': '[171,30.6094]'
    }
    img_size = '[200,44]'
    input_points = []
    args = str.split(' ')
    for i in range(len(args)):
        point = pointMap[args[i]]
        input_points.append(point)
    input_points = '[' + ','.join(input_points) + ']'
    captcha = "{\"img_size\":" + img_size + ",\"input_points\":"+ input_points+"}"
    return captcha
#print(get_xsrf())
#get_captcha()

#图片验证码登陆
def login(account, password):
    _xsrf = get_xsrf()
    captcha = str(get_picture())
    email_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': account,
        'password': password,
        '_xsrf': _xsrf,
        'captcha': captcha
        #'captcha_type' : 'cn'
    }
    headers['X-Xsrftoken'] = _xsrf
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Origin'] = 'https://www.zhihu.com'
    headers['Referer'] = 'https://www.zhihu.com/'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    print(headers)
    response = session.post(email_url, data=data, headers=headers)
    print(response)
    print('hhh')
    print(response.text)
    login_code = response.json()
    print(login_code)
    print(session.cookies)
    r = session.get("https://www.zhihu.com/settings/profile", headers=headers, allow_redirects=False)
    print(r.status_code)

#倒立汉字登陆
def login_new(account, password):
    _xsrf = get_xsrf()
    captcha = get_captcha()
    print(captcha)
    email_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': account,
        'password': password,
        '_xsrf': _xsrf,
        'captcha': captcha,
        'captcha_type': 'cn'
    }
    print(data)
    headers['X-Xsrftoken'] = _xsrf
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Origin'] = 'https://www.zhihu.com'
    headers['Referer'] = 'https://www.zhihu.com/'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    response = session.post(email_url, data=data, headers=headers)
    print(response)
    print('hhh')
    print(response.text)
    login_code = response.json()
    print(login_code)
    print(session.cookies)
    r = session.get("https://www.zhihu.com/settings/profile", headers=headers, allow_redirects=False)
    print(r.status_code)


if __name__ == '__main__':
    account = input('请输入你的邮箱\n>  ')
    password = input("请输入你的密码\n>  ")
    login_new(account=account, password=password)



