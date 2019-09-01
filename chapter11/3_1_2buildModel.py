
# coding: utf-8

# In[1]:

# 模型构建 C盘
# 详解BIC方式定信息准则　＋　ARIMA 
import pandas as pd
inputfile = 'attrsConstruction.xlsx'

data = pd.read_excel(inputfile)
df = data.iloc[:len(data)-5]
df


# In[2]:

# 第 * 1 * 步--C盘---------平稳性检测
#1)平稳性检测 ：判断是否平稳，若不平稳，对其进行差分处理直至平稳
# 方法：采用单位根检验（ADF）的方法或者时序图的方法（见数据探索模块）
# 注意：其他平稳性检验方法见steadyCheck.py文件
from statsmodels.tsa.stattools import adfuller as ADF
diff = 0
# 判断D盘数据的平稳性，以及确定几次差分后平稳
adf = ADF(df['CWXT_DB:184:C:\\'])
print adf 

while adf[1] >= 0.05 : # adf[1]是p值，p值小于0.05认为是平稳的
    print adf[1]
    diff = diff + 1
    adf = ADF(df['CWXT_DB:184:C:\\'].diff(diff).dropna())#注意，差分后使用ADF检验时，必须去掉空值
    
print (u'原始序列经过%s阶差分后归于平稳，p值为%s') % (diff, adf[1])
df['CWXT_DB:184:C:\\_adf'] = df['CWXT_DB:184:C:\\'].diff(1)


# In[3]:

# 第 * 2 * 步--C盘---------白噪声检验
# 目的：验证序列中有用信息是否已经被提取完毕，需要进行白噪声检验。若序列是白噪声序列，说明序列中有用信息已经被提取完，只剩随机扰动
# 方法：采用LB统计量的方法进行白噪声检验
# 若没有通过白噪声检验，则需要进行模型识别，识别其模型属于AR、MA还是ARMA。

inputfile2 = 'attrsConstruction.xlsx'
data1 = pd.read_excel(inputfile2)
data1 = data1.iloc[:len(data1)-5]# 不使用最后五个数据（作为预测参考）

# 白噪声检测
from statsmodels.stats.diagnostic import acorr_ljungbox

[[lb], [p]] = acorr_ljungbox(data1['CWXT_DB:184:C:\\'], lags = 1) ## lags是残差延迟个数
if p < 0.05:
    print (u'原始序列为非白噪声序列，对应的p值为：%s' % p)
else:
    print (u'原始序列为白噪声序列，对应的p值为：%s' % p)

[[lb], [p]] = acorr_ljungbox(data1['CWXT_DB:184:C:\\'].diff(1).dropna(), lags = 1)
if p < 0.05:
    print (u'一阶差分序列为非白噪声序列，对应的p值为：%s' % p)
else:
    print (u'一阶差分序列为白噪声序列，对应的p值为：%s' % p)


# In[4]:

# 第 * 3 * 步----------模型识别
# 方法：采用极大似然比方法进行模型的参数估计，估计各个参数的值。
# 然后针对各个不同模型，采用信息准则方法（有三种：BIC/AIC/HQ)对模型进行定阶，确定p,q参数，从而选择最优模型。
# 注意，进行此步时，index需要为时间序列类型
# 确定最佳p、d、q的值
inputfile3 = 'attrsConstruction.xlsx'
data2 = pd.read_excel(inputfile3,index_col='COLLECTTIME')
xtest_value=data2['CWXT_DB:184:C:\\'][-5:]
data2 = data2.iloc[:len(data2)-5]# 不使用最后五个数据（作为预测参考） 
# print data2
xdata2 = data2['CWXT_DB:184:C:\\']
# print xdata2
# ARIMA（p,d,q）中,AR是自回归,p为自回归项数；MA为滑动平均,q为滑动平均项数,d为使之成为平稳序列所做的差分次数(阶数)，由前一步骤知d=1
# from statsmodels.tsa.arima_model import ARIMA#建立ARIMA（p,d，q）模型
from statsmodels.tsa.arima_model import ARIMA #建立ARIMA（p,q）模型

# 定阶
# 目前选择模型常用如下准则!!!!!
# 增加自由参数的数目提高了拟合的优良性，
# AIC/BIC/HQ鼓励数据拟合的优良性但是尽量避免出现过度拟合(Overfitting)的情况。所以优先考虑的模型应是AIC/BIC/HQ值最小的那一个
#* AIC=-2 ln(L) + 2 k 中文名字：赤池信息量 akaike information criterion (AIC)
# * BIC=-2 ln(L) + ln(n)*k 中文名字：贝叶斯信息量 bayesian information criterion (BIC)
# * HQ=-2 ln(L) + ln(ln(n))*k hannan-quinn criterion (HQ)

# ----------------------------------------------------------
pmax = int(len(xdata2)/10) # 一般阶数不超过length/10
qmax = int(len(xdata2)/10) # 一般阶数不超过length/10

bic_matrix = [] # bic矩阵
for p in range(pmax+1):
    tmp = []
    for q in range(qmax+1):
        try:#存在部分为空值，会报错
#             print ARIMA(xdata2, (p,1,q)).fit().bic
            tmp.append(ARIMA(xdata2, (p,1,q)).fit().bic) #  BIC方式
        except:
            tmp.append(None)
            
    bic_matrix.append(tmp)
    
bic_matrix = pd.DataFrame(bic_matrix) # 从中可以找出最小值
print bic_matrix
print bic_matrix.stack()


# In[5]:

# 第 * 4 * 步--C盘---------模型检验
# 确定模型后，需要检验其残差序列是否是白噪声，若不是，说明，残差中还存在有用的信息，需要修改模型或者进一步提取。
# 若其残差不是白噪声，重新更换p,q的值，重新确定
import pandas as pd
import numpy as np

while 1:
    p, q = bic_matrix.stack().idxmin() # 先展平该表格，然后找出最小值的索引位置
    print (u'当前BIC最小的p值与q值分别为：%s、%s' % (p,q))
    
    lagnum = 12 # 残差延迟个数

    # 由模型识别可知第一次BIC最小的p值与q值分别为：0、1

    arima = ARIMA(xdata2, (p,1,q)).fit() # 建立并训练模型
    xdata_pred = arima.predict(typ = 'levels') # 预测
    pred_error = (xdata_pred - xdata2).dropna() # 计算残差

    # 白噪声检测
    from statsmodels.stats.diagnostic import acorr_ljungbox

    lbx, px = acorr_ljungbox(pred_error, lags = lagnum)
    h = (px < 0.05).sum() # p值小于0.05，认为是非噪声
    if h > 0:
        print (u'模型ARIMA(%s,1,%s)不符合白噪声检验' % (p,q))
        print ('在BIC矩阵中去掉[%s,%s]组合，重新进行计算' % (p,q))
        bic_matrix.iloc[p,q] =  np.nan
        arimafail = arima
        continue
    else:
        print (p,q)
        print (u'模型ARIMA(%s,1,%s)符合白噪声检验' % (p,q))
        break
        
        


# In[6]:

arima.summary() # 当p,q值为0，0时，summary方法报错


# In[7]:

forecast_values, forecasts_standard_error, forecast_confidence_interval = arima.forecast(5)
forecast_values


# In[8]:

predictdata = pd.DataFrame(xtest_value)
predictdata.insert(1,'CWXT_DB:184:C:\\_predict',forecast_values)
predictdata.rename(columns={'CWXT_DB:184:C:\\':u'实际值','CWXT_DB:184:C:\_predict':u'预测值'},inplace=True)
predictdata.info()


# In[9]:

result_d = predictdata.applymap(lambda x: '%.2f' % x) # 将表格中各个浮点值都格式化
result_d.to_excel('pedictdata_C_BIC_ARIMA.xlsx')
result_d


# In[10]:

# 第 * 5 * 步--D盘---------模型评价
# 为了评价时序预测模型效果的好坏，本章采用3个衡量模型预测精度的统计量指标：平均绝对误差、均方根误差、平均绝对百分误差
# -*- coding:utf-8 -*-
import pandas as pd

inputfile4 = 'pedictdata_C_BIC_ARIMA.xlsx'
result = pd.read_excel(inputfile4,index_col='COLLECTTIME')
result = result.applymap(lambda x: x/10**6)
print result

# 计算误差
abs_ = (result[u'预测值']-result[u'实际值']).abs()
mae_ = abs_.mean() # mae平均绝对误差
rmas_ = ((abs_**2).mean())**0.5 #rmas均方根误差
mape_ = (abs_/result[u'实际值']).mean() #mape平均绝对百分误差
# print abs_
print mae_
print rmas_
print mape_
errors = 1.5
print '误差阈值为%s' % errors
if (mae_ < errors) & (rmas_ < errors) & (mape_ < errors):
    print (u'平均绝对误差为：%.4f, \n均方根误差为：%.4f, \n平均绝对百分误差为：%.4f' % (mae_, rmas_, mape_))
    print '误差检验通过！'
else:
    print '误差检验不通过！'


# In[ ]:



