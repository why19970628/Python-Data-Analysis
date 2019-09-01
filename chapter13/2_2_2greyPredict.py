
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from GM11 import GM11 # 引入自己编写的灰色预测函数

inputfile1 = 'data2.csv'

data = pd.read_csv(inputfile1)
data.index = range(1999,2014)
data


# In[2]:

data.loc[2014] = None
data.loc[2015] = None
h = ['x1', 'x3', 'x5']
for i in h:
    gm = GM11(data[i][range(1999, 2014)].as_matrix())
    f = gm[0] ##获得灰色预测函数
    P = gm[-1] # 获得小残差概率
    C = gm[-2] # 获得后验比差值
    data[i][2014] = f(len(data)-1)
    data[i][2015] = f(len(data))
    data[i] = data[i].round(6) # 保留2位小数
    if (C < 0.35 and P > 0.95): # 评测后验差判别
        print '对于模型%s，该模型精度为---好' % i
    elif (C < 0.5 and P > 0.8):
        print '对于模型%s，该模型精度为---合格' % i
    elif (C < 0.65 and P > 0.7):
        print '对于模型%s，该模型精度为---勉强合格' % i
    else:
        print '对于模型%s，该模型精度为---不合格' % i
 


# In[3]:

#保存的表名命名格式为“2_2_2_k此表功能名称”，是此小节生成的第1张表格，功能为greyPredict：灰色预测
data[h+['y']].to_excel('2_2_2_1greyPredict.xlsx')


# In[4]:

data


# In[ ]:



