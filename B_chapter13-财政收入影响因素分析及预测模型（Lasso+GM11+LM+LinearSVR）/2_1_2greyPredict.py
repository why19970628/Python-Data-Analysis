
# coding: utf-8

# In[1]:


# 2_1 某市财政收入预测模型
# 灰色预测：灰色预测是一种对含有不确定因素的系统进行预测的方法，灰色预测通过鉴别系统因素之间发展趋势的相异程度，即进行关联分析，
# 并对原始数据进行生成处理来寻找系统变动的规律，生成有较强规律性的数据序列，然后建立相应的微分方程模型，从而预测事物未来发展趋势的状况。
# 其用等时距观测到的反应预测对象特征的一系列数量值构造灰色预测模型，预测未来某一时刻的特征量，或达到某一特征量的时间。
# 灰色理论建立的是生成数据模型，不是原始数据模型
# 数据生成方式：A：累加生成：通过数列间各时刻数据的依个累加得到新的数据与数列。累加前数列为原始数列，累加后为生成数列。B：累减生成 C：其他
# 优势：是处理小样本数据预测问题的有效工具
import pandas as pd
import numpy as np
from GM11 import GM11 # 引入自己编写的灰色预测函数

inputfile1 = 'data1.csv'

data = pd.read_csv(inputfile1)
data.index = range(1994,2014)
data


# In[2]:


# 灰色预测函数
def GM11(x0): #自定义灰色预测函数  #该函数覆盖了导入的包的同名函数
    import numpy as np
    x1 = x0.cumsum() #1-AGO序列
    z1 = (x1[:len(x1)-1] + x1[1:])/2.0 #紧邻均值（MEAN）生成序列 # 由常微分方程可知，取前后两个时刻的值的平均值代替更为合理
    # x0[1] = -1/2.0*(x1[1] + x1[0])
    z1 = z1.reshape((len(z1),1))
    B = np.append(-z1, np.ones_like(z1), axis = 1) # (***)
    Yn = x0[1:].reshape((len(x0)-1, 1))
    [[a],[b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Yn) #计算参数
#     fkplusone = (x1[0]-b/a)*np.exp(-a*k)#时间响应方程 # 由于x0[0] = x1[0]
    f = lambda k: (x1[0]-b/a)*np.exp(-a*(k-1))-(x1[0]-b/a)*np.exp(-a*(k-2)) #还原值 
    delta = np.abs(x0 - np.array([f(i) for i in range(1,len(x0)+1)])) # 残差
    C = delta.std()/x0.std() # 后验比差值
    P = 1.0*(np.abs(delta - delta.mean()) < 0.6745*x0.std()).sum()/len(x0)
    return f, a, b, x0[0], C, P #返回灰色预测函数、a、b、首项、方差比、小残差概率


# In[3]:

data.loc[2014] = None
data.loc[2015] = None
h = ['x1', 'x2', 'x3', 'x4', 'x5', 'x7']
P = []
C = []
for i in h:
    gm = GM11(data[i][range(1994, 2014)].as_matrix())
    f = gm[0] ##获得灰色预测函数
    P = gm[-1] # 获得小残差概率
    C = gm[-2] # 获得后验比差值
    data[i][2014] = f(len(data)-1)
    data[i][2015] = f(len(data))
    data[i] = data[i].round(2) # 保留2位小数
    if (C < 0.35 and P > 0.95): # 评测后验差判别
        print '对于模型%s，该模型精度为---好' % i
    elif (C < 0.5 and P > 0.8):
        print '对于模型%s，该模型精度为---合格' % i
    elif (C < 0.65 and P > 0.7):
        print '对于模型%s，该模型精度为---勉强合格' % i
    else:
        print '对于模型%s，该模型精度为---不合格' % i


# In[4]:

#保存的表名命名格式为“2_1_2_1k此表功能名称”，是此小节生成的第1张表格，功能为greyPredict：灰色预测

data[h+['y']].to_excel('2_1_2_1greyPredict.xlsx')


# In[5]:

data


# In[ ]:



