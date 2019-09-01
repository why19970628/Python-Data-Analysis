
# coding: utf-8

# In[1]:


# 2_1 某市财政收入预测模型
# 2_1_1 变量选择模型，本小节中书中使用的是AdaptiveLasso，但是没有找到该函数，所以采用了其他变量选择模型
# 书中给出的选出的变量为'x1', 'x2', 'x3', 'x4', 'x5', 'x7'
import pandas as pd
import numpy as np
inputfile1 = 'data1.csv'
data = pd.read_csv(inputfile1)
data # 1994到2013年间的各个影响因素的数据


# In[ ]:

# # 注意：此段代码无法运行：没有找到该函数
# # 导入AdaptiveLasso包
# from sklearn.linear_model import AdaptiveLasso
# model = AdaptiveLasso(gamma = 1)
# model.fit(data.iloc[:, 0:13], data['y'])
# model.coef_# 各个特征的系数


# In[3]:

from sklearn.linear_model import Lasso# AdaptiveLasso找不到
# LASSO回归的特点是在拟合广义线性模型的同时进行变量筛选和复杂度调整。 因此，不论目标因变量是连续的，还是二元或者多元离散的，
#都可以用LASSO回归建模然后预测。 这里的变量筛选是指不把所有的变量都放入模型中进行拟合，而是有选择的把变量放入模型从而得到更好的性能参数。
model = Lasso(alpha=0.1)
model.fit(data[['x1', 'x2', 'x3', 'x4','x5', 'x7']], data['y']) # data.iloc[:, 0:13]
print model.coef_ # 各个特征的系数
print model.intercept_


# In[4]:

from sklearn.linear_model import Lars #最小角回归
model1 = Lars(n_nonzero_coefs = 7)
model1.fit(data.iloc[:, 0:13], data['y'])
print model1.coef_ # 各个特征的系数


# In[5]:

# 确定最合适的Alpha
from sklearn.linear_model import LarsCV #交叉验证最小二乘法回归模型
model1 = LarsCV()
model1.fit(data.iloc[:, 0:13], data['y'])
print model1.coef_ # 各个特征的系数
print model1.alpha_


# In[6]:

from sklearn.linear_model import LassoCV #交叉验证最小二乘法回归模型
model1 = LassoCV()
model1.fit(data.iloc[:, 0:13], data['y'])
print model1.coef_ # 各个特征的系数
print model1.alpha_


# In[8]:

from sklearn.linear_model import Lasso# AdaptiveLasso找不到
# LASSO回归的特点是在拟合广义线性模型的同时进行变量筛选和复杂度调整。 因此，不论目标因变量是连续的，还是二元或者多元离散的，
#都可以用LASSO回归建模然后预测。 这里的变量筛选是指不把所有的变量都放入模型中进行拟合，而是有选择的把变量放入模型从而得到更好的性能参数。
model = Lasso(alpha = 0.1)
model.fit(data.iloc[:,:13], data['y']) # data.iloc[:, 0:13]
print model.coef_ # 各个特征的系数
print model.intercept_


# In[9]:

# 分析合适的Lasso变量组合
import itertools
from sklearn.linear_model import Lasso   # AdaptiveLasso找不到
import time 
start = time.clock()
a = data.columns[:13]
tempdf = pd.DataFrame([])
for i in range(1,len(a)+1):
    All = list(itertools.combinations(a,i))
    for j in range(len(All)):
        model = Lasso(alpha=0.1)
        model.fit(data[list(All[j])], data['y']) # data.iloc[:, 0:13]
        effect = model.intercept_
        tempdf = tempdf.append([str(list(All[j])), effect])
end = time.clock()
print '耗费时间为' + str(end-start) +'s!'

res1 = pd.DataFrame(tempdf[tempdf.index == 1 ][0])
res1.columns = ['lassovalue']
res1.head() # len(res)=8191
res1['index'] = tempdf[tempdf.index == 0 ][0].values
res = res1.set_index('index')
res['absLasso'] = np.abs(res['lassovalue'].values)
res.sort_values(by = 'absLasso')


# In[10]:

# 岭回归（Ridge 回归）
from sklearn import linear_model
clf = linear_model.Ridge(alpha=0.1)  # 设置k值
clf.fit(data.iloc[:, 0:13], data['y'])  # 参数拟合
print(clf.coef_)  # 系数
print(clf.intercept_)  # 常量
# print(clf.predict([[3, 3]]))  # 求预测值

print(clf.score(data.iloc[:, 0:13], data['y']))  # R^2，拟合优度
print(clf.get_params())  # 获取参数信息
print(clf.set_params(fit_intercept=False))  # 重新设置参数 


# In[ ]:



