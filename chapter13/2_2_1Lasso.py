
# coding: utf-8

# In[1]:


# 2_2 增值税预测模型
import pandas as pd
import numpy as np
inputfile1 = 'data2.csv'
data = pd.read_csv(inputfile1)
data # 1994到2013年间的各个影响因素的数据
# 本小节中书中使用的是AdaptiveLasso，但是没有找到该函数，所以采用了其他变量选择模型
# 书中给出的选出的变量为'x1', 'x3', 'x5'


# In[2]:

# # 注意：此段代码无法运行：没有找到该函数
# # 导入AdaptiveLasso包
# from sklearn.linear_model import AdaptiveLasso
# model = AdaptiveLasso(gamma = 1)
# model.fit(data.iloc[:, 0:6], data['y'])
# model.coef_# 各个特征的系数


# In[2]:

from sklearn.linear_model import Lasso
# LASSO回归的特点是在拟合广义线性模型的同时进行变量筛选和复杂度调整。 因此，不论目标因变量是连续的，还是二元或者多元离散的，
#都可以用LASSO回归建模然后预测。 这里的变量筛选是指不把所有的变量都放入模型中进行拟合，而是有选择的把变量放入模型从而得到更好的性能参数。
model = Lasso(alpha=0.1)
model.fit(data[['x1', 'x2', 'x3', 'x4','x5', 'x6']], data['y']) # data.iloc[:, 0:13]
model.coef_ # 各个特征的系数


# In[3]:

model.intercept_


# In[4]:

# 通过Lasso得到的变量为 x1、x3、x5
model = Lasso(alpha=0.1)
model.fit(data[['x1', 'x3','x5']], data['y']) # data.iloc[:, 0:13]
model.coef_ # 各个特征的系数


# In[ ]:




# In[ ]:



