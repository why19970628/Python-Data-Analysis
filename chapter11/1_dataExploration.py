
# coding: utf-8

# In[1]:


#数据探索分析

import pandas as pd
import numpy as np
from pandas import DataFrame,Series


# In[2]:

inputfile1 = 'discdata.xls'
data = pd.read_excel(inputfile1)
data.head()


# In[3]:

data.info()


# In[4]:

d = data[(data['ENTITY']=='C:\\') & (data['TARGET_ID']==184 )]
d


# In[5]:

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rc('figure',figsize=(9,7))
import datetime
import matplotlib.dates as mdates
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']= False


# In[6]:

fig  = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title(u"C盘已使用空间的时序图")
# ax.set_xlabel(u'日期')
ax.set(xlabel=u'日期',ylabel=u'磁盘使用大小')
# 图上时间间隔显示为10天
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32), interval=10)) 
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.subplots_adjust(bottom=0.13,top=0.95)
ax.plot(d['COLLECTTIME'],d['VALUE'],'ro-',)

fig.autofmt_xdate() #自动根据标签长度进行旋转
'''for label in ax.xaxis.get_ticklabels():   #此语句完成功能同上
       label.set_rotation(45)
'''
plt.savefig('c.jpg')
plt.show()


# In[7]:

d1 = data[(data['ENTITY']=='D:\\') & (data['TARGET_ID']==184 )]
d1


# In[ ]:




# In[8]:

fig  = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title(u"D盘已使用空间的时序图")
# ax.set_xlabel(u'日期')
ax.set(xlabel=u'日期',ylabel=u'磁盘使用大小')
# 图上时间间隔显示为10天
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32), interval=10)) 
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.subplots_adjust(bottom=0.13,top=0.95)
ax.plot(d1['COLLECTTIME'],d1['VALUE'],'g*-',)

fig.autofmt_xdate() #自动根据标签长度进行旋转
'''for label in ax.xaxis.get_ticklabels():   #此语句完成功能同上
       label.set_rotation(45)
'''
plt.savefig('d.jpg')
plt.show()


# In[ ]:

# 通过图中可以发现，磁盘的使用情况都不具有周期性，表现出缓慢性增长，呈现趋势性。因此，可以初步确认数据是非平稳的

