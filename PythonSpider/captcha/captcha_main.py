#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : captcha_main.py
# @Author: Hui
# @Date  : 2017/10/19
# @Desc  :

'''
#本程序用于验证码的暴力破解，针对特定的网站
#流程如下：
1.爬取验证码
2.将验证码进行图片预处理，去除噪点
3.将验证码分割成单一字符
4.运用已经训练好的模型，进行预测
'''

from picture import download_captcha, image_to_binary, img_segment
from svm_features import get_feature_vector
from cfg import SVM_CAPTCHA_MODEL, CRACK_PATH, CAPTCHA_URL
from svmutil import *
from PIL import Image
import os
import uuid

#函数主入口
if __name__=='__main__':
    for cc in range(10):
        name = str(uuid.uuid1())
        #1.取得验证码
        image_path = download_captcha(CAPTCHA_URL, name+'.jpg')
        #2.图片预处理
        bin = image_to_binary(image_path)
        #3.图片分割
        seg_list = img_segment(bin)
        index = 1
        captcha = ''
        #4.运用svm训练的模型进行预测
        for i in seg_list:
            x = get_feature_vector(i)
            y = [9]
            model = svm_load_model(SVM_CAPTCHA_MODEL)
            p_label, p_acc, p_val = svm_predict(y, x, model)
            captcha += str(p_label[0]).split('.')[0]
        captcha_path = image_path.replace(name, '__'+captcha+'__'+str(uuid.uuid1()))
        #5.将预测的结果保存为图片的文件名
        os.rename(image_path, captcha_path)
        print('验证码结果:%s' %(captcha))
        #print(cc)
    print('验证码爬虫识别程序结束....感谢您的使用')