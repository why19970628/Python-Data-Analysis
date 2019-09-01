# -*- coding:utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
# a = range(1,5)
# b = range(5,9)
# c = range(9,13)
# x = [[]]
# x.append(a)
# print x
# x.append(b)
# print x
# x.append(c)
# print x
# del x[0]
# print x
# # print np.ndarray(a)
# df =  DataFrame(x,columns=list('abcd'))
# print df
# #
#
# print df
# print a,b,c

import os
# cur_path = os.path.abspath(os.curdir)
# s = os.getcwd()
# os.mkdir(goal_path)
# print cur_path,s


# 输出图片输出目录：
def saveimg(dstpath):
    # dstpath = raw_input('请输入图片输出目录：')
    if (os.path.exists(dstpath) == False) and  dstpath != '': # 若输入的路径不存在，则创建该目录
        os.makedirs(dstpath)  # 创建目标文件夹
    if dstpath == '': #不输入路径(直接回车）则表示使用源图片所在目录
        dstpath = os.getcwd()
    return dstpath

#请输入图片输出目录
# dstpath = saveimg()
dstpath = saveimg(raw_input('请输入图片输出目录：'))
print dstpath