
# coding: utf-8


import pandas as pd
from pandas import DataFrame
import numpy as np


# 读取类型1的表格中的颜色矩数据
d1 = pd.read_csv('type1.csv',encoding="gbk")
# 读取类型2的表格中的颜色矩数据
d2 = pd.read_csv('type2.csv',encoding="gbk")
# 读取类型3的表格中的颜色矩数据
d3 = pd.read_csv('type3.csv',encoding="gbk")
# 读取类型4的表格中的颜色矩数据
d4 = pd.read_csv('type4.csv',encoding="gbk")
# 读取类型5的表格中的颜色矩数据
d5 = pd.read_csv('type5.csv',encoding="gbk")

ALLDATA = pd.concat([d1,d2,d3,d4,d5],ignore_index=True) # 做表格连接
ALLDATA.to_excel('ALLDATA.xlsx',index=False) # 存储数据

