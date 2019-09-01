
# coding: utf-8

# In[1]:

import pandas as pd
inputfile = 'attrsConstruction.xlsx'

data = pd.read_excel(inputfile)
df = data.iloc[:len(data)-5]

inputfile1 = 'pedictdata_C.xlsx'# 预测值
result = pd.read_excel(inputfile1)
inputfile2 = 'pedictdata_D.xlsx'# 预测值
result1 = pd.read_excel(inputfile2)


import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rc('figure',figsize=(9,9))
import datetime
import matplotlib.dates as mdates
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']= False


# In[2]:

data.head()


# In[3]:

fig  = plt.figure()

fig.set(alpha=0.2)#设置图标透明度

ax = fig.add_subplot(2,1,1)
ax.set_title(u"C盘空间时序预测图")

ax.set(xlabel=u'日期',ylabel=u'磁盘使用大小')
# 图上时间间隔显示为10天
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32), interval=7)) 
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.subplots_adjust(bottom=0.13,top=0.95)
ax.plot(df['COLLECTTIME'],df['CWXT_DB:184:C:\\'],'ro--',)
ax.plot(result['COLLECTTIME'],result[u'实际值'],'g+--',)
ax.plot(result['COLLECTTIME'],result[u'预测值'],'b*-',)
ax.grid(axis='y',linestyle='--')
ax.legend()
fig.autofmt_xdate() #自动根据标签长度进行旋转
'''for label in ax.xaxis.get_ticklabels():   #此语句完成功能同上
       label.set_rotation(45)
'''

ax1 = fig.add_subplot(2,1,2)
ax1.set_title(u"D盘空间时序预测图")
# ax.set_xlabel(u'日期')
ax1.set(xlabel=u'日期',ylabel=u'磁盘使用大小')
# 图上时间间隔显示为10天
ax1.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32), interval=7)) 
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.subplots_adjust(bottom=0.13,top=0.95)
ax1.plot(df['COLLECTTIME'],df['CWXT_DB:184:D:\\'],'co--',)
ax1.plot(result1['COLLECTTIME'],result1[u'实际值'],'m+--',)
ax1.plot(result1['COLLECTTIME'],result1[u'预测值'],'y*-',)
ax1.grid(axis='y',linestyle='--')
ax1.legend()
fig.autofmt_xdate() #自动根据标签长度进行旋转
'''for label in ax.xaxis.get_ticklabels():   #此语句完成功能同上
       label.set_rotation(45)
'''
plt.savefig('data_predict_pic.jpg')
plt.show()


# In[4]:

result


# In[ ]:




# In[ ]:



