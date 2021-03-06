#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : picture.py
# @Author: Hui
# @Date  : 2017/10/18
# @Desc  :

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import time
import uuid
import pytesseract
from PIL import Image
from PIL import ImageEnhance
import PIL.ImageOps
import sys
from cfg import CAPTCHA_URL, CRACK_PATH
import os

#下载网上的验证码，并保存为file名字的文件
def download_captcha(URL, file):
    '''
    :param URL: 抓取的验证码URL
    :param file: 验证码存储的文件名
    :return: 返回图片存储的路径
    '''
    time.sleep(2)
    image_path = os.path.join(CRACK_PATH, file)
    urlretrieve(URL, image_path)
    return image_path

def download_tieta():
    for i in range(1000,2000):
        image_src = CAPTCHA_URL
        urlretrieve(image_src, 'image_tieta/'+str(i)+'.jpg')
        time.sleep(5)
        sys.stdout.write('\r')
        sys.stdout.write("%s%% |%s" % (int(i % 1000), int(i % 1000) * '#'))
        sys.stdout.flush()
    print('tieta captcha finish')

def initTable(threshold=220):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


#预处理图片为二值图，降低图片的维度。
#此步骤做完后，图片的预处理基本工作也已经完成
#此处只是展示了一个简单的例子，关于验证码图片处理目前有了很好的方法，CNN卷积神经网络
def image_to_binary(img_path):
        '''
        :param img_path: 验证码的路径
        :return: 返回PIL.image
        '''
        im = Image.open(img_path)
        #im = Image.open('image_tieta/'+str(i)+'.jpg')
        # 去除四周的边框
        box = (1,1,im.size[0]-1,im.size[1]-1)
        im = im.crop(box)
        #im = no_black(im)
        im = ImageEnhance.Contrast(im).enhance(5)  #增加对照度
        im = im.convert('L')            #灰度化

        im = im.point(initTable(), '1')  #二值化

        #去除噪点
        im = set_round(im)
        im = clear_noise(im)
        im = clear_line_noise(im)
        #im.save('image_deal/' + str(i) + '.jpg')
        #vcode = pytesseract.image_to_string(im)
        #print('%d.jpg: %s' %(i, vcode))
        return im

#对原图验证码的噪点做简单的处理，
#此种方法其实属于歪门邪道，当验证码的字符颜色和噪点的颜色接近时，就失效；
#我一开始处理的验证码字符为彩色，噪点为黑色，所以可以简单的投机一下，
#最后验证码去噪的结果还不错，不过适应性有限。
def no_black(im):
    black = 30   #此处的值为0-255
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            tmp = im.getpixel((x,y))
            if (tmp[0] < black)&(tmp[1]<black)&(tmp[2]<black):
                im.putpixel((x,y), (255,255,255))
    return im

#1.扫描二值图，查看噪点附近相连接的黑色点数；若发现越少则说明，该点可能
#为离散点的可能行越高。
#2.阈值调优。
def clear_noise(im):
    width, height = im.size
    for x in range(1, width-1):
        for y in range(1, height-1):
            black_point = 0
            count = 0
            flag = False
            mid_pixel = im.getpixel((x,y))
            #判断黑点周围的黑点数量情况
            if mid_pixel == 0:
                point_1 = im.getpixel((x - 1, y - 1))
                point_2 = im.getpixel((x - 1, y))
                point_3 = im.getpixel((x - 1, y + 1))
                point_4 = im.getpixel((x, y - 1))
                point_5 = im.getpixel((x, y + 1))
                point_6 = im.getpixel((x + 1, y - 1))
                point_7 = im.getpixel((x + 1, y))
                point_8 = im.getpixel((x + 1, y + 1))

                if point_1 == 0:
                    black_point += 1
                if point_2 == 0:
                    black_point += 1
                if point_3 == 0:
                    black_point += 1
                if point_4 == 0:
                    black_point += 1
                if point_5 == 0:
                    black_point += 1
                if point_6 == 0:
                    black_point += 1
                if point_7 == 0:
                    black_point += 1
                if point_8 == 0:
                    black_point += 1
                if black_point <= 1:
                    im.putpixel((x, y), 1)

    return im

#消除干扰线
def clear_line_noise(im):
    width, height = im.size
    for x in range(1, width-1):
        for y in range(1, height-1):
            black_point = 0
            count = 0
            flag = False
            mid_pixel = im.getpixel((x,y))
            #判断黑点周围的黑点数量情况
            if mid_pixel == 0:
                point_1 = im.getpixel((x - 1, y - 1))
                point_2 = im.getpixel((x - 1, y))
                point_3 = im.getpixel((x - 1, y + 1))
                point_4 = im.getpixel((x, y - 1))
                point_5 = im.getpixel((x, y + 1))
                point_6 = im.getpixel((x + 1, y - 1))
                point_7 = im.getpixel((x + 1, y))
                point_8 = im.getpixel((x + 1, y + 1))
                #统计四条直线，此方法用于针对噪点为干扰线的验证码
                if point_1==1 & point_8==1:
                    count += 1
                if point_2==1 & point_7==1:
                    count += 1
                if point_3==1 & point_6==1:
                    count += 1
                if point_4==1 & point_5==1:
                    count += 1
                if count >= 3:
                    im.putpixel((x, y), 1)
    return im

#将二值图四周边框设置为1
def set_round(im):
    width, height = im.size
    for x in range(0,width-1):
        im.putpixel((x,0), 1)
        im.putpixel((x,height-1), 1)
    for y in range(0, height-1):
        im.putpixel((0, y), 1)
        im.putpixel((width-1, y), 1)
    return im



#再完成图片预处理之后，我们进行图片分割，将图片切割成单个字符的图片
#这一步具有针对性，我选取的验证码比较常规，具有一定的切割规律可寻
#若碰上歪斜的验证码，则本切割程序失效，应该另寻办法解决。

def img_segment(img):
    '''
    :param img: PIL.Image
    :return: PIL.Image
    '''
    img_seg = []
    for i in range(4):
        x = 5 + i * (12 + 3)
        y = 1
        img_tmp = img.crop((x, y, x+12, y+17))
        img_seg.append(img_tmp)

    return img_seg

def generate_sample():
    for i in range(1000):
        im = Image.open('image_deal/' + str(i) + '.jpg')
        im_1,im_2,im_3,im_4 = img_segment(im)
        im_1.save('image_seg/' + str(i)+'_1.gif')
        im_2.save('image_seg/' + str(i) + '_2.gif')
        im_3.save('image_seg/' + str(i) + '_3.gif')
        im_4.save('image_seg/' + str(i) + '_4.gif')

if __name__ == '__main__':
    #image_to_binary()
    #download_tieta()
    #generate_sample()
    print('sample ok')


