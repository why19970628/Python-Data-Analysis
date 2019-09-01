#####求间隔时间的另外一种方式，把每个用水事件中切割出多个只含水流量=0的事件，然后，计算内部每个小的水流量为0的小块的间隔
# 时间间隔 = 与上条不为0的数据的间隔/2 + （本段间隔结束时间-本段间隔开始时间） + 与下条不为0的数据的间隔/2 
# coding: utf-8

import pandas as pd
import numpy as np
from pandas import DataFrame
inputfile = 'data_exchange_divideEvent.xlsx'
data = pd.read_excel(inputfile)
inputfile1 = 'data_guiyue.xlsx'
data1 = pd.read_excel(inputfile1)
x = pd.merge(data1,data[[u'用水停顿时间间隔',u'事件编号']],left_index = True, right_index=True,how='outer')
x.to_excel('attr_const_for_gap.xlsx')

ifile = 'attr_const_for_gap.xlsx'
df = pd.read_excel(ifile)
# 将数据划分成一次用水事件！（*****）
l=list(df[u'事件编号'])
Adf = DataFrame([], columns = df.columns)# 创建一个空列表
pos=-1
MX = int(df[u'事件编号'].max())
for j in range(MX):
    y = []
    for i in range(l.count(j+1)):
        pos=l.index(j+1,pos+1)
        y.append(pos)
    a = min(y)
    b = max(y)
    temp = df.iloc[a:b+1,:]
    Adf = pd.concat([Adf,temp])
Adf[u'事件编号'].fillna(method='ffill',inplace = True)
Adf[[u'水流量']] = Adf[[u'水流量']].astype('float64')
Adf['gap'] = Adf[u'发生时间'].diff()
Adf.to_excel('gap_time_compute.xlsx')

data_all = Adf

#-----*第 1 种方法*-----
def gap_time(x):
    gap_time = pd.Timedelta(seconds = 0)
    if len(x) ==1:
        gap_time = gap_time
    else:
        i=0
        tempdf = DataFrame([])
        while i< len(x)-1:
            i= i+1
            if (x.loc[x.index[i],u'水流量']) == 0:
                tempdf = tempdf.append(x.ix[x.index[i],:])
                if (x.loc[x.index[i+1],u'水流量']) != 0:
                    start = tempdf.loc[tempdf.index[0],u'发生时间']    
                    end = tempdf.loc[tempdf.index[-1],u'发生时间']
                    b = list(x.index).index(tempdf.index[0])-1
                    start_gap = x.iloc[b,0]
                    c = list(x.index).index(tempdf.index[-1])+1
                    end_gap = x.iloc[c,0]
#                     print start_gap,start,end,end_gap
                    t1 = (start-start_gap)/2
                    t2 = (end_gap-end)/2
                    t3 = end-start
                    t = t1+t2+t3
#                     print t1,t2,t3,t
                    gap_time = gap_time+t
    
                    tempdf = DataFrame([])
    
    gap_time = gap_time/np.timedelta64(1,'s') # 将间隔时间转成“秒”
    return gap_time

dt_list = []
for n in range(1,int(data_all[u'事件编号'].max())+1):
    dt = gap_time(data_all[data_all[u'事件编号'] == n] )
    dt_list.append(dt)
print dt_list

#-----*第 2 种方法*-----
# 第二种方法：
def gap_time_2(y):
    gap_time_2 = pd.Timedelta(seconds = 0)
    templist = []
    for i in range(len(y)):
        if y.iloc[i,6] == 0:
            templist.append(i)
    if (len(y) ==1) | (templist==[]):
        gap_time_2 = gap_time_2
    else:
        for j in templist:
            gap_time_2 = gap_time_2 + y.iloc[j,-1]/2 + y.iloc[j+1,-1]/2
            
    return gap_time_2/np.timedelta64(1,'s')
gp_list = []
for n in range(1,int(data_all[u'事件编号'].max())+1):
    gp = gap_time_2(data_all[data_all[u'事件编号'] == n] )
    gp_list.append(gp)
print gp_list  

# 计算用水时间
def use_time(y):
    send_time = pd.Timedelta(seconds = 2)
    use_time = pd.Timedelta(seconds = 0)
    templist = []
    for i in range(len(y)):
        if y.iloc[i,6] != 0:
            templist.append(i)
    if len(y) ==1:
        use_time = send_time
    else:
        for j in templist:
            if j == 0:
                use_time = use_time + y.iloc[j+1,-1]/2 + send_time/2
            elif j == (len(y)-1):
                use_time = use_time + y.iloc[j,-1]/2 + send_time/2
            else:
                use_time = use_time + y.iloc[j,-1]/2 + y.iloc[j+1,-1]/2
    return use_time/np.timedelta64(1,'s')
dt_list = []
for n in range(1,int(data_all[u'事件编号'].max())+1):
    dt = use_time(data_all[data_all[u'事件编号'] == n] )
    dt_list.append(dt)
print dt_list


#-----*第 3 种方法*-----
df2 = data_all 
# 确定一次用水时间和停顿时间
dtest =  DataFrame(df2[[u'事件编号',u'水流量']],columns=[u'事件编号',u'水流量'])
dtest['realindex'] = range(len(df2[u'事件编号']))
dtest
l=list(dtest[u'事件编号'])
pos=-1

useTIME = []
gapTIME = [] 

for j in range(int(data_all[u'事件编号'].max())):
    TIME = pd.Timedelta(seconds = 0)
    y = []
    for i in range(l.count(j+1)):
        pos=l.index(j+1,pos+1)
        y.append(pos)
    a = min(y)#出现值i最小的index````````
    b = max(y)#出现值i最大的index
    n =0   
    tgap = dtest.iloc[a:b+1,:]
#     print tgap
    TG = tgap[tgap[u'水流量']==0]
    if (a==b) | (len(TG)==0):
        TIME = TIME
    else:
        th = 1
        d = TG['realindex'].diff() > th
        TG[u'tgtimes'] = d.cumsum() + 1
        z = list(TG[u'tgtimes'])
        OP = []
        pos1=-1
        for m in range(TG[u'tgtimes'].max()):
            y1 = []
            for m1 in range(z.count(m+1)):
                pos1 =z.index(m+1,pos1+1)
                y1.append(pos1)
            c = min(y1)#出现值i最小的index````````
            d = max(y1)#出现值i最大的index
            c0 = TG.index[c]
            c1 = list(df2.index).index(c0)
            c2 = c1-1
            d0 = TG.index[d]
            d1 = list(df2.index).index(d0)
            d2 = d1+1
#             print c,d,c0,d0,c1,d1,c2,d2
            stu1 = (df2.iloc[c1,0]-df2.iloc[c2,0])/2# 设置用水开始时间=起始数据时间-发送阈值/2
            enu1 = (df2.iloc[d2,0]-df2.iloc[d1,0])/2# 设置用水开始时间=起始数据时间-发送阈值/2
            meu1 = df2.iloc[d1,0]-df2.iloc[c1,0]
            tempgap = enu1+stu1+meu1
            TIME = TIME + tempgap
    gaptime= TIME/np.timedelta64(1, 's')
    gapTIME.append(gaptime)

print gapTIME





#----------------以下都是测试代码---------------------
x = data_all[data_all[u'事件编号'] == 8]

gap_time = pd.Timedelta(seconds = 0)
# print len(x)
if len(x) ==1:
    gap_time = gap_time
else:
    i=0
    tempdf = DataFrame([])
    while i< len(x)-1:
        i= i+1
        if (x.loc[x.index[i],u'水流量']) == 0:
            tempdf = tempdf.append(x.ix[x.index[i],:])
            if (x.loc[x.index[i+1],u'水流量']) != 0:
                start = tempdf.loc[tempdf.index[0],u'发生时间']    
                end = tempdf.loc[tempdf.index[-1],u'发生时间']
                b = list(x.index).index(tempdf.index[0])-1
                start_gap = x.iloc[b,0]
                c = list(x.index).index(tempdf.index[-1])+1
                end_gap = x.iloc[c,0]
                print start_gap,start,end,end_gap
                tempdf = DataFrame([])
                t1 = (start-start_gap)/2
                t2 = (end_gap-end)/2
                t3 = end-start
                t = t1+t2+t3
                print t1,t2,t3,t
                gap_time = gap_time+t
print gap_time            
# tempdf      
# print tempdf.loc[tempdf.index[0],u'发生时间']    # 间隔时间开始
# print tempdf.loc[tempdf.index[-1],u'发生时间'] # 间隔时间结束
# # a = tempdf.index[0]
# b = list(x.index).index(a)-1
# # c = list(x.index).index(a)+1
# # print a,b,c
# d = x.iloc[b,0]# 间隔时间开始前一刻
# # e = x.iloc[c,0]


# print d
# print '--1--'
# a1 = tempdf.index[-1]
# b1 = list(x.index).index(a1)-1
# c1 = list(x.index).index(a1)+1
# # print a1,b1,c1
# # d1 = x.iloc[b1,0]
# e1 = x.iloc[c1,0]# 间隔时间结束后一刻
# print e1
# print '--2--'


# In[129]:

df = DataFrame(np.arange(12).reshape(3,4),columns=list('abcd'))
df.iloc[1:2,3]=np.nan
df['d'].fillna(method='ffill',inplace=True)
tempdf = DataFrame([])
# tempdf.ix[]= df.ix[2,:]
# tempdf[1]= df.ix[2,:]
tempdf = tempdf.append(df.ix[2,:])
tempdf = tempdf.append(df.ix[1,:])
tempdf = tempdf.append(df.ix[1,:])
tempdf.append(df.ix[0,:])
# tempdf = DataFrame([])
tempdf.iloc[-1,0]
tempdf


# In[70]:

x.loc[x.index[1],[u'水流量']]


# In[74]:

x.loc[x.index[1],u'水流量']


# In[81]:

x.ix[x.index[1],:]


# In[91]:

x.iloc[-1,0]


# In[89]:

x.head()


# In[90]:

x.tail()


# In[106]:

x[x[u'水流量']== 0]


# In[ ]:



