#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : svm_predict.py
# @Author: Hui
# @Date  : 2017/10/19
# @Desc  :

from svm import svm_problem, svm_parameter
from svmutil import *
from cfg import SVM_CAPTCHA_MODEL, SVM_TRAINING_DATA, SVM_TEST_DATA

def svm_data_demo():
    """
    这个是来自于网上的demo，和本识图项目无关
    :return:
    """
    y = [1, -1]  # 训练数据的标签
    x = [{1: 1, 2: 1}, {1: -1, 2: -1}]  # 训练数据的输入向量
    # <label> <index1>:<value1> <index2>:<value2>
    # 相当于找到的特征值

    prob = svm_problem(y, x)  # 定义SVM模型的训练数据
    param = svm_parameter('-t 0 -c 4 -b 1')  # 训练SVM模型所需的各种参数
    model = svm_train(prob, param)  # 训练好的SVM模型

    # svm_save_model('model_file', model)#将训练好的模型保存到文件中

    # 使用测试数据集对已经训练好的模型进行测试
    yt = [-1]  # 测试数据标签
    xt = [{1: 1, 2: 1}]  # 测试数据输入向量

    p_label, p_acc, p_val = svm_predict(yt, xt, model)

    """
    - p_label:预测标签的列表
    - p_acc 存储预测的精确度,均值和回归的平方相关系数
    - p_vals 在指定参数‘-b 1’时将返回的判定系数（判定的可靠程度）
    """

    print(p_label)

#生成训练模型
def train_model(training_data, model_path):
    '''
    :param training_data: 训练数据的路径
    :param model_path: 模型保存的路径
    :return:
    '''
    y,x = svm_read_problem(training_data)
    model = svm_train(y, x)
    svm_save_model(model_path, model)

def test_model(test_data, model_path):
    '''
    :param test_data: 测试数据路径
    :param model_path: 运用模型的路径
    :return:
    '''
    y, x = svm_read_problem(test_data)
    model = svm_load_model(model_path)
    p_label, pacc, p_val = svm_predict(y, x, model)
    print(p_label)


if __name__=='__main__':
    train_model(SVM_TRAINING_DATA, SVM_CAPTCHA_MODEL)
    #test_model(SVM_TEST_DATA, SVM_CAPTCHA_MODEL)
    print('generate model')
