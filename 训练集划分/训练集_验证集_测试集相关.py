#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from sklearn.model_selection import KFold
import numpy as np
import os
import shutil
import random
import math
import re
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
                if i < math.floor(0.9 * len(filenames)):  # math.floor  向下取整
                    sub_path = os.path.join(path2, str(n) ,'train')  # 训练集
                    isExists = os.path.exists(sub_path)   #判断是否存在sub_path这个路径---->肯定没有~阿巴
                    if not isExists:  # 如果不存在则创建目录
                        #创建目录操作函数
                        os.makedirs(sub_path)
                    shutil.copy(os.path.join(path, filenames[i]), sub_path)  #把打乱的数据一个一个复制粘贴过去
                else:
                    sub_path = os.path.join(path2, str(n) , 'test')  # 测试集
                    isExists = os.path.exists(sub_path)   #同上
                    if not isExists:
                        os.makedirs(sub_path)
                    shutil.copy(os.path.join(path, filenames[i]), sub_path)
    return 0
#-----提取BIEOS标签内容-----
def BIEOS(txt):
    # 先全标注为O--->O_ODOIO_O_O申O报O地O区O或O单O位O：O北O京O  （最开始多了一个O)
    normal_list = re.sub('','\tO\n',txt)   #(替换条件,替换后,替换前)
    list1 = re.sub('^\tO\n','',normal_list)  #删去最开始多的O----一定要加^开始条件！！
    list1 = re.sub('<\tO\nI\tO\nC\tO\nH\tO\n-\tO\nT\tO\nE\tO\nR\tO\nM\tO\n>\tO','<ICH-TERM>',list1)
    bieos_list = re.findall('<ICH-TERM>\n(.+?)\n<ICH-TERM>',list1,re.S)  #(匹配项,txt)
    # print(bieos_list)--->['八\tO\n达\tO\n岭\tO',……]
    for lst in bieos_list:
        # print(lst)
        length = lst.count('\t')   #数数
        if length == 1:   #八\tO
            lst2 = lst[0] + '\t' + 'S'
        else:   #八\tO\n达\tO
            lst2 = lst[0] + '\t' + 'B' + lst[3:-2] + '\tE'
            lst2 = lst2.replace('\tO','\tI')
        list1 = list1.replace('<ICH-TERM>\n%s\n<ICH-TERM>'%lst,lst2)  #(old,new)
    list1 = list1.replace('。\tO\n','。\tO\n\n')
    list1 = list1.replace('？\tO\n','？\tO\n\n')
    list1 = list1.replace('！\tO\n','！\tO\n\n')
    list1 = list1.replace('……\tO\n','……\tO\n\n')
    return list1
#-----BIEOS序列标签转换，输出txt-----
def BIEOS_change(path2):
        for new_sub_dir in range(1,11):   # print(new_sub_dir)  #文件夹的名称1,2,3……
            print('正在处理第',new_sub_dir,'个文件')
            filenames = ['test','train']
            for son in filenames:   #1,2,3……底下的test和train---->print(son)----test
                read_path = os.path.join(path2,str(new_sub_dir),son)    #'.\data_processed\1'
                write_path = os.path.join(path2,str(new_sub_dir),str(son)+'.txt')   #print(write_path)--->'.\data_processed\1\test.txt'
                fileArray = []
                for root, dirs, files2 in os.walk(read_path):
                    processed_txt = ''  # 放每个test||train的总内容
                    #其中，root为根目录路径，dirs是root路径下的目录列表，files为root路径下的文件列表
                    for f in files2:
                        eachpath = str(root + '/' + f)
                        fileArray.append(eachpath)
                        # print(fileArray)
                        # -->'.\\data_processed\\1\\test/12O.txt'
                        with open(eachpath, 'r', encoding='utf-8')as f:
                            group_txt = f.read()
                            # print(group_txt)
                            processed_txt += BIEOS(group_txt)  #读一个加一个~
                    with open(write_path, 'w', encoding='utf-8')as f2:
                        f2.write(processed_txt)
def main():
    path1 = r'..\data'
    path2 = r'.\data_processed'
    k_fold(path1,path2)  #语料文件划分
    BIEOS_change(path2)  #标签转换，输出
if __name__ == '__main__':
    main()
