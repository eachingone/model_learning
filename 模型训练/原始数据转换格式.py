#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sklearn.model_selection import KFold
import numpy as np
import os
import shutil
import random
import math
import re
import xlrd
import csv
#-----k-fold交叉验证-----
def k_fold(path1,path2):
    if os.path.exists(path1) == 1:#文件夹存在，则新建一个新的文件夹
        os.makedirs(path2)
    else:
        print('文件夹不存在！')
        return 1
    for n in range(1,11):
        for path, sub_dirs, files in os.walk(path1):  # 文件夹下三层文件，三级文件夹的路径
            filenames = os.listdir(path1)  # filmenames 这时就是每个二级文件下每个文件的名字
            filenames = list(filter(lambda x: x.endswith('.txt'),filenames))  # 把flimnames = x ,此时以.txt结尾的文件通过过滤器 ，filter语法，后接函数还有序列 第一个为判断函数，第二个为序列
            random.shuffle(filenames)  # 把序列中所有元素，随机排序得到一个打乱了的列表
            for i in range(len(filenames)):
                if i < math.floor(0.8 * len(filenames)):  # math.floor  向下取整

                    sub_path = os.path.join(path2, str(n) ,'train.tsv')  # 训练集
                    isExists = os.path.exists(sub_path)   #判断是否存在sub_path这个路径---->肯定没有~阿巴
                    # if not isExists:  # 如果不存在则创建目录
                    #     #创建目录操作函数
                    #     os.makedirs(sub_path)
                    new_filename = os.path.join(path,filenames[i],sub_path)
                    print(sub_path)
                    shutil.copy(os.path.join(path, filenames[i]), sub_path)  #把打乱的数据一个一个复制粘贴过去
                elif i < math.floor(0.9 * len(filenames)):
                    sub_path = os.path.join(path2, str(n), 'test.tsv')  # 测试集
                    isExists = os.path.exists(sub_path)  # 同上
                    if not isExists:
                        os.makedirs(sub_path)
                    shutil.copy(os.path.join(path, filenames[i]), sub_path)
                else:
                    sub_path = os.path.join(path2, str(n) , 'dev.tsv')  # 测试集
                    isExists = os.path.exists(sub_path)   #同上
                    if not isExists:
                        os.makedirs(sub_path)
                    shutil.copy(os.path.join(path, filenames[i]), sub_path)
    return 0

def main():
    # path1 = r'..\data'
    # path2 = r'.\data_processed'

    # path1 = r'..\..\任务2\任务二_郑依晴\data'
    # path2 = r'..\..\任务2\任务二_郑依晴\data_processed'
    path3 = r'..\样例数据.xlsx'
    path4 = r''
    #读取excel，将每一行单独写成txt
    xl = xlrd.open_workbook(path3)
    table = xl.sheet_by_name('Sheet1')
    row = table.nrows
    for i in range(1,11):
        path = os.path.join(path4+str(i))
        os.mkdir(path)
        path_dev = os.path.join(path + '\dev.tsv')
        path_train = os.path.join(path + '\\train.tsv')
        num = list(range(1,row+1))
        random.shuffle(num)   #这一步不需要赋值
        for n in range(1,row):
            biaoqian = table.row_values(n)[5]
            biaoqian = biaoqian[0]
            jvzi = table.row_values(n)[6]
            jvzi = jvzi.replace('\n','')
            if n<math.floor(0.8*row):
               with open(path_train, 'a+',encoding='utf-8',newline='') as f:
                   tsv_w = csv.writer(f, delimiter='\t')
                   tsv_w.writerow([biaoqian,jvzi])   #writelines
            else:
                with open(path_dev, 'a+',encoding='utf-8',newline='') as f:
                    tsv_w = csv.writer(f, delimiter='\t')
                    tsv_w.writerow([biaoqian,jvzi])

    # k_fold(path1,path2)  #语料文件划分
if __name__ == '__main__':
    main()
