
# coding: utf-8

# In[1]:

# -*- utf-8 -*-
# 1 数据抽取
# 2 数据探索分析
#   通过频率分布直方图分析用户用水停顿时间间隔的规律性--->探究划分一次完整用水事件的时间间隔阈值
# 
# 3 数据预处理
# （1）数据规约 data_guiyue.py
# -*- utf-8 -*-
# 规约掉"热水器编号"、"有无水流"、"节能模式"三个属性
# 注意：
#书中提到：规约掉热水器"开关机状态"=="关"且”水流量”==0的数据，说明热水器不处于工作状态，数据记录可以规约掉。但由后文知，此条件不能进行规约
# 因为，"开关机状态"=="关"且”水流量”==0可能是一次用水中的停顿部分，删掉后则无法准确计算关于停顿的数据


# In[2]:

import pandas as pd
import numpy as np
from pandas import DataFrame
or_data = pd.read_excel('original_data.xls',encoding='gbk')
or_data.head()


# In[3]:

data = or_data.drop(or_data.columns[[0,5,9]],axis=1) # 删掉不相关属性
data.head()


# In[4]:

data.info()


# In[5]:

data[u'发生时间'] = pd.to_datetime(data[u'发生时间'], format = '%Y%m%d%H%M%S')#将时间列转成日期格式（***）
print len(data)
# 由后文知，此条件无用
# data1 = data[(data[u'开关机状态']==u'开')|(data[u'水流量']!=0)]
# data1.head()
data.head(10)


# In[6]:

data.to_excel('data_guiyue.xlsx')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



