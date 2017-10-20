#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : svm_features.py
# @Author: Hui
# @Date  : 2017/10/19
# @Desc  :

'''
#生成svm的向量文件，图片的大小为 12 * 17的大小
#x_ = 12, y_=17
#在此我们选择29维度，即每一个维度选用行数的黑点数量
#9 1:4 2:2 3:2 4:2 5:3 ... 29:6
'''

import pytesseract
from PIL import Image
import sys
from cfg import WORK_PATH, SVM_TRAINING_DATA, SVM_TEST_DATA
import os
import re

#得到图片的特征值
def get_feature(im):
    width, height = im.size
    feature_list = []
    for x in range(width):
        count = 0
        for y in range(height):
            if im.getpixel((x,y)) == 0:
                count += 1
        feature_list.append(count)

    for y in range(height):
        count = 0
        for x in range(width):
            if im.getpixel((x,y)) == 0:
                count += 1
        feature_list.append(count)
    #转化为text
    text = ''
    for i in range(len(feature_list)):
        text += str(i+1) + ':' + str(feature_list[i])
        text += ' '
    return text

#得到特征值的vector
def get_feature_vector(im):
    width, height = im.size
    feature_list = []
    for x in range(width):
        count = 0
        for y in range(height):
            if im.getpixel((x,y)) == 0:
                count += 1
        feature_list.append(count)

    for y in range(height):
        count = 0
        for x in range(width):
            if im.getpixel((x,y)) == 0:
                count += 1
        feature_list.append(count)
    #转化为vector
    vector = []
    dict = {}
    for i in range(len(feature_list)):
        dict[i+1] = feature_list[i]
    vector.append(dict)
    return vector

#生成svm的训练数据
def generate_svm_train_data(key, dest_path):
    #针对图片生成训练数据
    result = open(dest_path, 'w+')
    record = 0
    for data_dir in os.listdir(WORK_PATH):
        data_path = os.path.join(WORK_PATH, data_dir)
        if os.path.isdir(data_dir):
            if data_dir.startswith(key):
                for f in os.listdir(data_path):
                    image_path = os.path.join(data_path, f)
                    pattern = key + r'(.*?)/'
                    label = re.findall(pattern, image_path)[0]
                    im = Image.open(image_path)
                    feature = get_feature(im)
                    #特征数据写入文件
                    result.write(label + ' ' + feature)
                    result.write('\n')
                    record += 1
    result.close()
    print('生成训练数据完成，总共生成%d条数据，路径:%s' %(record, dest_path))
    return record


if __name__=='__main__':
    generate_svm_train_data('crack_', SVM_TRAINING_DATA)
    #generate_svm_train_data('test_data_', SVM_TEST_DATA)
    print('haha')