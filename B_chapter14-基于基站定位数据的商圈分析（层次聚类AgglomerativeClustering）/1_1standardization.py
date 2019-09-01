
# coding: utf-8

# In[1]:

#-*- utf-8 -*-
# 离差标准化（最大最小规范化）：保留了原来数据中存在的关系，消除梁刚和数据取值范围影响最简单的方法
# 目标：消除数量级数据带来的影响，数据标准化到[0,1]
import pandas as pd

filename = 'business_circle.xls'
data = pd.read_excel(filename, index_col = u'基站编号')
data = (data - data.min()) / (data.max() - data.min()) # 离差标准化
data.to_excel('1_1standardization.xlsx')
data


# In[ ]:



