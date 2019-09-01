
# coding: utf-8

# In[1]:

# data_exchange_divideEvent.py
# 一次完整用水事件的划分模型
# 方法：判断流量大于0的记录的时间差是否超过阈值，是，则是两次事件，否，则是一次事件
# -*- utf-8 -*-
# 第一步：探索划分一次完整用水事件的时间间隔阈值
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
plt.rc('figure',figsize=(9,6))
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

inputfile = 'data_guiyue.xlsx'
outputfile ='dataExchange_divideEvent.xlsx'


data = pd.read_excel(inputfile)

data[u'发生时间'] = pd.to_datetime(data[u'发生时间'], format = '%Y%m%d%H%M%S')#（***）
data = data[data[u'水流量'] > 0] # 只要流量大于0的记录
# print len(data) #7679

data[u'用水停顿时间间隔']= data[u'发生时间'].diff()/ np.timedelta64(1, 'm') #将datetime64[ns]转成 以分钟为单位（*****）
data= data.fillna(0)# 替换掉data[u'用水停顿时间间隔']的第一个空值
data.head()


# In[2]:

#-----第*2*步-----数据探索，查看各数值列的最大最小和空值情况
data_explore = data.describe().T
data_explore['null'] = len(data)-data_explore['count']
explore = data_explore[['min','max','null']]
explore.columns = [u'最小值',u'最大值',u'空值数']
explore


# In[3]:

#        最小值   最大值   空值 
# 水流量   8.0  77.000000 0.0
# 用水停顿时间间隔0.0 2093.366667 0.0

#----第*3*步-----离散化与面元划分
# 将时间间隔列数据划分为0~0.1，0.1~0.2，0.2~0.3....13以上，由数据描述可知，
# data[u'用水停顿时间间隔']的最大值约为2094，因此取上限2100
Ti = list(data[u'用水停顿时间间隔'])#将要面元化的数据转成一维的列表
timegaplist = [0.0,0.1,0.2,0.3,0.5,1,2,3,4,5,6,7,8,9,10,11,12,13,2100]# 确定划分区间

cats = pd.cut(Ti,timegaplist,right=False) # 包扩区间左端,类似"[0,0.1)",（默认为包含区间右端）
x = pd.value_counts(cats)
x.sort_index(inplace = True)
dx = DataFrame(x,columns=['num'])
dx['fn'] = dx['num']/sum(dx['num'])
dx['cumfn'] = dx['num'].cumsum()/sum(dx['num'])

f1 = lambda x :'%.2f%%' %  (x*100)
dx[['f']]= dx[['fn']].applymap(f1)
dx


# In[4]:

#-----第*4*步-----画用水停顿时间间隔频率分布直方图
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

dx['fn'].plot(kind='bar')
plt.ylabel(u'频率/组距')
plt.xlabel(u'时间间隔（分钟）')
p = 1.0*dx['fn'].cumsum()/dx['fn'].sum()# 数值等于 dx['cumfn']，但类型是列表
dx['cumfn'].plot(color = 'r', secondary_y = True, style = '-o',linewidth = 2)
plt.annotate(format((p[4]), '.4%'), xy = (7, p[4]), xytext=(7*0.9, p[4]*0.95), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) #添加注释，即85%处的标记。这里包括了指定箭头样式。
plt.ylabel(u'累计频率')

plt.title(u'用水停顿时间间隔频率分布直方图')
plt.grid(axis='y',linestyle='--')

# fig.autofmt_xdate() #自动根据标签长度进行旋转
for label in ax.xaxis.get_ticklabels():   #此语句完成功能同上,但是可以自定义旋转角度
       label.set_rotation(60)

plt.savefig('Water-pause-times.jpg')
plt.show()


# In[5]:

#-----第*5*步-----：确定一次用水事件停顿阈值后，开始划分一次完整事件
threshold = pd.Timedelta(minutes=4)#阈值为四分钟
d = data[u'发生时间'].diff() > threshold # 相邻时间做差分，比较是否大于阈值（*****）
data[u'事件编号'] = d.cumsum() + 1 # 通过累积求和的方式为事件编号（*****）

data.to_excel(outputfile)
                         


# In[6]:

data.head()


# In[ ]:




# In[ ]:




# In[ ]:



