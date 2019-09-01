
# coding: utf-8

# 2> 模型建立

# -*- coding:utf-8 -*-
from __future__ import print_function
import pandas as pd
from pandas import DataFrame,Series
from selfapriori import * # 导入自行编写的Apriori函数
import time# 导入时间库来计算用时

# inputfile ='apriori.txt' #输入事务集文件
# '''apriori.txt中文件格式如下
# A1,B2,C1,D3,E2,F1,H2
# A2,B2,C1,D2,E2,F1,H3
# A3,B4,C2,D3,E4,F1,H4
# A3,B1,C2,D1,E1,F1,H1
# '''
# data2 = pd.read_csv(inputfile, header=None, dtype=object)
data2 = pd.read_excel('apriori.xlsx', header=0)

start = time.clock() # 计时开始
print(u'\n转换原始数据至0-1矩阵')

ct = lambda x: Series(1, index = x[pd.notnull(x)]) # 将标签数据转换成1，是转换0-1矩阵的过渡函数
b = map(ct, data2.as_matrix())# 用map方式执行
data2 = DataFrame(b).fillna(0)
end = time.clock() #计时开始

print (u'转换完毕，用时%s秒' % (end-start))
del b #删除中间变量b 节省内存

support = 0.06 #最小支持度
confidence = 0.75 #最小置信度
ms = '---'# 用来区分不同元素，需要保证原始表格中无该字符

start = time.clock() #计时开始
print(u'\n开始搜索关联规则...')
find_rule(data2, support, confidence, ms)
end = time.clock() 
print (u'\n搜索完成，用时：%.2f秒' % (end-start))

