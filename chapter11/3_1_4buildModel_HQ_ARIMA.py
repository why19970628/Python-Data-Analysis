
# coding: utf-8

# In[1]:

# 模型构建 C盘
import pandas as pd
inputfile = 'attrsConstruction.xlsx'

data = pd.read_excel(inputfile)
df = data.iloc[:len(data)-5]


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
# 然后针对各个不同模型，采用BIC信息准则对模型进行定阶，确定p,q参数，从而选择最优模型。
# 注意，进行此步时，index需要为时间序列类型
# 确定最佳p、d、q的值
inputfile3 = 'attrsConstruction.xlsx'
data2 = pd.read_excel(inputfile3,index_col='COLLECTTIME')
xtest_value=data2['CWXT_DB:184:C:\\'][-5:]
data2 = data2.iloc[:len(data2)-5]# 不使用最后五个数据（作为预测参考） 
xdata2 = data2['CWXT_DB:184:C:\\']
# ARIMA（p,d,q）中,AR是自回归,p为自回归项数；MA为滑动平均,q为滑动平均项数,d为使之成为平稳序列所做的差分次数(阶数)，由前一步骤知d=1
from statsmodels.tsa.arima_model import ARIMA#建立ARIMA（p,1，q）模型

# 定阶
# 目前选择模型常用如下准则!!!!!
#* AIC=-2 ln(L) + 2 k 中文名字：赤池信息量 akaike information criterion (AIC)
# * BIC=-2 ln(L) + ln(n)*k 中文名字：贝叶斯信息量 bayesian information criterion (BIC)
# * HQ=-2 ln(L) + ln(ln(n))*k hannan-quinn criterion (HQ)
# 增加自由参数的数目提高了拟合的优良性，
# AIC/BIC/HQ鼓励数据拟合的优良性但是尽量避免出现过度拟合(Overfitting)的情况。所以优先考虑的模型应是AIC/BIC/HQ值最小的那一个

# 方法三：HQ方式----------------------------------------------------------
pmax = int(len(xdata2)/10) # 一般阶数不超过length/10
qmax = int(len(xdata2)/10) # 一般阶数不超过length/10

hq_matrix = [] # hq矩阵
for p in range(pmax+1):
    tmp = []
    for q in range(qmax+1):
        try:
            print ARIMA(xdata2, (p,1,q)).fit().hq
            tmp.append(ARIMA(xdata2, (p,1,q)).fit().hq) #存在部分为空值，会报错,所以加上异常控制
        except:
            tmp.append(None)
            
    hq_matrix.append(tmp)
    
hq_matrix = pd.DataFrame(hq_matrix) # 从中可以找出最小值
print hq_matrix
print hq_matrix.stack()

# 说明：由于用HQ训练模型时，都是空值，所以，本例使用HQ不合适


# In[8]:




# In[9]:




# In[10]:




# In[11]:




# In[12]:




# In[13]:




# In[ ]:



