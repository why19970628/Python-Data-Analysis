
# coding: utf-8

# In[1]:

# dataExchange_attributeConstruction

# 目标：属性构造和洗浴事件筛选
# 需要构造的属性如下：
#热水事件	起始数据编号	终止数据编号	开始时间（begin_time）
# 根据日志判断是否为洗浴（1表示是，0表示否）	洗浴时间点	总用水时长（w_time）	
# 总停顿时长（w_pause_time）	平均停顿时长（avg_pause_time）	停顿次数（pause）	
# 用水时长（use_water_time）	用水/总时长（use_water_rate）	总用水量（w_water）
# 平均水流量（water_rate）	水流量波动（flow_volatility）	停顿时长波动（pause_volatility）

import pandas as pd
import numpy as np
from pandas import DataFrame,Series


inputfile = 'dataExchange_divideEvent.xlsx'
data = pd.read_excel(inputfile)
# len(data)# 7696
inputfile1 = 'data_guiyue.xlsx'
data1 = pd.read_excel(inputfile1)
x = pd.merge(data1,data[[u'事件编号']],left_index = True, right_index=True,how='outer')
# 连接'data_guiyue.xlsx'和 'dataexchange_divideEvent.xlsx'的后两列,因为，属性规约里面包含水流量为0的数值，
# 后一个表中，只含有水流量不为0的值，需要将两边进行连接，获知规约后的数据中的数据所属的事件数,利用处理后的数开始进行数据构造工作
x.head()#18840
x.to_excel('data_for_attr_const.xlsx')


# In[2]:

df = pd.read_excel('data_for_attr_const.xlsx')
# 将数据划分成一次用水事件！（*****）
#-----第*1*步-----做基本处理，获取用于构造属性的数据表
# 将数据划分成一次用水事件！（*****）
# 思路：获取每个事件的序号值所在的最小的index值和最大的index值，然后将其连接，
# 即： 去掉不同事件间的“事件编号”为空的值，保留同一个事件内的“事件编号”为空的值
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
Adf[u'事件编号'].fillna(method='ffill',inplace = True) # 向后填充，填上了事件编号的空值
Adf[[u'水流量']] = Adf[[u'水流量']].astype('float64')
Adf.to_excel('1TimeWaterDivide.xlsx')
Adf.head()


# In[3]:

#-----第*2*步-----建立存放构造的属性的表
df2 = pd.read_excel('1TimeWaterDivide.xlsx')
df2['gap'] = df2[u'发生时间'].diff()
MX = int(df2[u'事件编号'].max())# 获取当前事件数172
fdf2 = DataFrame([], index = range(1,MX+1))# 创建一个空列表 用来存放属性规约结果


# In[4]:

#-----第*3*步-----开始构造属性
#构造属性第一部分：包含用水事件开始编号、用水事件结束编号、用水开始时间、用水结束时间、用水总时间、用水间隔时间、一次用水期间“水流量”为0的记录数
fdf2.index.names = ['eventNUM']

fdf2['stDataIndex'] = np.nan #用水事件开始编号
fdf2['edDataIndex'] = np.nan #用水事件结束编号
fdf2['stUseTime'] = np.nan #用水开始时间
fdf2['enUseTime'] = np.nan #用水结束时间
fdf2['AllUseTime'] = np.nan #用水总时间
fdf2['gapTimes'] = np.nan #用水间隔时间
fdf2['stopLines'] = np.nan # 一次用水期间“水流量”为0的记录数

ds = pd.Timedelta(seconds = 2) # 发送阈值时间设置为2秒
pos=-1# 标记变量     ******
l=list(df2[u'事件编号'])

# 以下空列表均是暂时存储数据
stUI = []
enUI = []
startU = []
endU = []
allUT = []
gapTS = []
stopLines = []
for j in range(MX):
    # 计算事件编号j在列表中的最开始出现的index和最后出现的index
    y = []# 存储时间编号j出现的所有的index（临时存储）
    for i in range(l.count(j+1)):
        pos=l.index(j+1,pos+1)
        y.append(pos)
    a = min(y)#出现值i最小的index
    b = max(y)#出现值i最大的index
    
    #记录一次用水的开始事件编号、结束事件编号
    stui= df2.index[a]
    enui= df2.index[b]
    stUI.append(stui)
    enUI.append(enui)
    
    #记录一次用水开始时间、结束时间
    stu = df2.iloc[a,0]-ds/2 # 设置用水开始时间=起始数据时间-发送阈值/2
    enu = df2.iloc[b,0]+ds/2 # 设置结束用水时间=结束数据时间+发送阈值/2
    startU.append(stu)
    endU.append(enu)
    
    #记录一次用水总时长
    allut = enu-stu
    allUT.append(allut)
    
    #判断停顿的行数（一次事件中水流量为0的记录的条数）
    stpts = df2.iloc[a:b+1,:]
    f =list(stpts[u'水流量'])
    stpt = f.count(0)#计算空值的个数
    stopLines.append(stpt)
  
    n =0   
    #判断停顿次数，中间有一个或多个空值均算作一次停顿
    if a==b :
        n=0
    else:
        tgap = df2.iloc[a:b+1,:]
        for t in range(a,b):
            g = tgap.ix[df2.index[t],[u'水流量']].values
            g1 = tgap.ix[df2.index[t+1],[u'水流量']].values
            if g1 == 0 and g!= 0:
                n+=1
    gapTS.append(n)
    
fdf2['stUseTime'] = startU
fdf2['enUseTime'] = endU
fdf2['stDataIndex'] = stUI
fdf2['edDataIndex'] = enUI
fdf2['AllUseTime'] = allUT
fdf2['gapTimes'] =gapTS
# 将一次用水事件的总时间转成以秒计
fdf2['AllUseTime(s)']= fdf2['AllUseTime']/np.timedelta64(1, 's')
fdf2['stopLines']= stopLines


# In[5]:

# 构造属性第二部分：获取用水的时间点的小时数，即洗浴时间点
fdf2['WashHour'] = np.nan

for i in range(1,len(fdf2['stUseTime'])+1):
    temp = fdf2.ix[i,'stUseTime'].strftime('%Y-%m-%d %H:%M:%S')# 将时间格式转成字符串,通过字符串截取获得时间点
    c = temp[11:13]
    d =int(c)
    fdf2.ix[i,'WashHour'] = d


# In[6]:

# 构造属性第三部分：确定一次用水时间和停顿时间、总用水量、水流量波动、平均用户水量
fdf2['UseTime'] = np.nan # 用水时间
fdf2['GapTime'] = np.nan # 停顿时间
fdf2['w_water'] = np.nan # 总用水量
fdf2['flow_volatility'] = np.nan # 水流量波动
fdf2['water_rate'] = np.nan #平均用水量


# 计算停顿时间（具体所有方法见time_gap_compute.py，此处采用的是第二种方法)
def gap_time_2(y):
    gap_time_2 = pd.Timedelta(seconds = 0)
    templist = []
    allgap = 0
    # 获取一次用水时间中间隔的行编号
    for i in range(len(y)):
        if y.iloc[i,6] == 0:
            templist.append(i)
    # 计算停顿时间    
    if (len(y) ==1) | (templist==[]):# 如果该事件只有一个或者两个非零用水记录，直接让用水停顿时间等于0
        gap_time_2 = gap_time_2
    else:
        for j in templist:# 采用书上公式：每条用水数据时长的和=（和上条数据的间隔时间/2+和下条数据的间隔时间/2）的和
            gap_time_2 = gap_time_2 + y.iloc[j,-1]/2 + y.iloc[j+1,-1]/2
    gap_time = gap_time_2/np.timedelta64(1,'s')
    

    return gap_time

# 计算用水时间 和 总用水量
def use_time(y):
    send_time = pd.Timedelta(seconds = 2) # 定义信息发送延迟时间为2秒
    use_time = pd.Timedelta(seconds = 0)
    templist = []
    w_water = 0 # 记录总用水量
    # 获取一次用水时间用水的行编号
    LASTIME = []#记录每个用水记录的持续用水时间
    for i in range(len(y)):# 将所有用水量不为0的记录的行号进行记录
        if y.iloc[i,6] != 0:
            templist.append(i)
    if len(y) ==1:# 如果用水量不为0的仅为1条，则用水时间为发送时间，用水持续时间为发送时间
        use_time = send_time
        lastime = send_time
        w_water = lastime/np.timedelta64(1,'s')* y.iloc[0,6]# 该次用水量为用水持续时间*水流量
        LASTIME.append(lastime/np.timedelta64(1,'s'))
    else:
        lastime = pd.Timedelta(seconds = 0)#用水时间=每条用水数据时长的和=（和上条数据的时间间隔/2+和下条数据的时间间隔/2）的和
        for j in templist:
            if j == 0:# 每一个用水事件开始时刻的用水持续时间=和下条数据的时间间隔/2+发送时间/2
                lastime = y.iloc[j+1,-1]/2 + send_time/2
            elif j == (len(y)-1):#每一个用水事件最后时刻的用水持续时间=和上条数据的时间间隔/2+发送时间/2
                lastime = y.iloc[j,-1]/2 + send_time/2
            else:
                lastime = y.iloc[j,-1]/2 + y.iloc[j+1,-1]/2
            use_time = use_time + lastime
            w_water = w_water + lastime/np.timedelta64(1,'s')* y.iloc[j,6]
            LASTIME.append(lastime/np.timedelta64(1,'s'))
      
    usetime = use_time/np.timedelta64(1,'s')
    avg = w_water/usetime# 平均水流量=总用水量/总用水时间
    
    allwater = 0 # 计算水流量波动 = sum((单次水流的值-平均水流量)**2*持续时间)/总用水时间
    if len(y) ==1:
        allwater = (y.iloc[0,6]-avg)**2
    else:
        for i in range(len(templist)):
            allwater = allwater + LASTIME[i]*(y.iloc[templist[i],6]-avg)**2 
    flow_vola = allwater/100/usetime# 水流量波动 # 此处除以100为了让数字看起来正常点，符合原作者给出的配书中给的数据值
        
    return usetime, w_water/100, avg, flow_vola


useTIME = []# 用水时间
gapTIME = []# 间隔时间
w_wat = []# 总用水量
flow_volatility = []# 水流量波动
avg_water_rate = [] # 平均水流量
for n in range(1,int(MX+1)):
    gp= gap_time_2(df2[df2[u'事件编号'] == n])
    use,w_water,avg,flow_vola = use_time(df2[df2[u'事件编号'] == n])
    gapTIME.append(gp)
    useTIME.append(use)
    w_wat.append(w_water)
    flow_volatility.append(flow_vola)
    avg_water_rate.append(avg)
    
fdf2['GapTime'] = gapTIME  
fdf2['UseTime'] = useTIME # fdf2['AllUseTime(s)']- fdf2['GapTime']
fdf2['w_water'] = w_wat
fdf2['water_rate'] = avg_water_rate
fdf2['flow_volatility'] = flow_volatility 

fdf2.head()


# In[7]:

# 构造属性第四部分：计算停顿时长波动
fdf2['pause_volatility'] = np.nan
pause_volatility = [] # 停顿时长波动
# 获取事件编号为eventnum的停顿次数
def get_gaptimes(eventnum):
    return fdf2['gapTimes'][eventnum] 

# 计算得出停顿时间和停顿时长波动（具体所有方法见time_gap_compute.py，此处采用的是第一种方法），因为这样可以算出单次停顿的具体时间
# 停顿时长波动=sum((单次停顿时长-平均停顿时长)**2*持续时间)/总停顿时间
def gap_time(x,gapTimes):
    gap_time = pd.Timedelta(seconds = 0)
    GAPTIME = []
    pause_vola = 0
    if len(x) ==1:
        gap_time = gap_time
        pause_vola = 0
    else:
        i=0
        tempdf = DataFrame([])
        while i< len(x)-1:
            i= i+1
            if (x.loc[x.index[i],u'水流量']) == 0:#若第i条水量为0
                tempdf = tempdf.append(x.ix[x.index[i],:])# 存储所有水流量为0的数据的记录
                if (x.loc[x.index[i+1],u'水流量']) != 0:# 若第i+1条水量不为0，说明这是一次停顿的结束
                    start = tempdf.loc[tempdf.index[0],u'发生时间']    # 计算该次停顿的开始时刻
                    end = tempdf.loc[tempdf.index[-1],u'发生时间']     # 计算该次停顿的结束时刻
                    b = list(x.index).index(tempdf.index[0])-1# 获取该次停顿发生的前一个用水量非0的记录的index
                    start_gap = x.iloc[b,0]
                    c = list(x.index).index(tempdf.index[-1])+1# 获取该次停顿结束的后一个用水量非0的记录的index
                    end_gap = x.iloc[c,0]
#                     print start_gap,start,end,end_gap
                    tempdf = DataFrame([]) # 清空tempdf，以记录下一次停顿时间
                    t1 = (start-start_gap)/2 # 停顿开始时与上一条非零数据的时间间隔/2
                    t2 = (end_gap-end)/2# 停顿结束时与下一条非零数据的时间间隔/2
                    t3 = end-start # 中间停顿时间
                    t = t1+t2+t3
#                     print t1,t2,t3,t
                    gap_time = gap_time+t
                    GAPTIME.append(t/np.timedelta64(1,'s'))#将每一小段的停顿时间存入，以计算停顿时长波动
    gap_time = gap_time/np.timedelta64(1,'s') # 将停顿时间转成“秒”
    # 计算平均停顿时间 = 总停顿时间/停顿次数
    if gapTimes != 0:# 若停顿次数不为0
        avg = gap_time/gapTimes 
    else:# 若停顿次数为0，则平均停顿时间等于停顿的时间
        avg = gap_time
    
    Allgap=0# 所有的停顿时间
    for i in range(len(GAPTIME)):
        Allgap = Allgap + GAPTIME[i]*(GAPTIME[i]-avg)**2
    pause_vola = Allgap/gap_time# 水流量波动
    return gap_time, pause_vola

for n in range(1,MX+1):
    gp, pause_vola = gap_time(df2[df2[u'事件编号'] == n], get_gaptimes(n))   
    pause_volatility.append(pause_vola)

fdf2['pause_volatility'] = pause_volatility 
fdf2.head()


# In[8]:

# 构造属性第五部分：一次用水事件中，用水时长的所占比重
fdf2['use_water_rate'] = fdf2['UseTime']/fdf2['AllUseTime(s)']
# 平均停顿时间
# fdf2['avg_pause_time'] = fdf2['GapTime']/fdf2['gapTimes']# 不能这样除，除数可能为0
fdf2['avg_pause_time'] = np.nan
for i in range(1,len(fdf2)+1):
    if fdf2.ix[i,['gapTimes']].values[0] != 0:
        fdf2.ix[i,['avg_pause_time']] = fdf2.ix[i,['GapTime']].values[0] / fdf2.ix[i,['gapTimes']].values[0]
    else :
        fdf2.ix[i,['avg_pause_time']] = 0

fdf2.head()


# In[9]:

# 属性构造结束，将各列重命名，然后保存
fdf2.rename(columns={'stDataIndex':u'起始数据编号','edDataIndex':u'终止数据编号','stUseTime':u'开始时间','enUseTime':u'结束时间',                  'AllUseTime':u'总用水时长（w_time）', 'gapTimes':u'停顿次数（pause）','stopLines':u'停顿行数','AllUseTime(s)':                     u'所有使用时间总用水时长（s）','WashHour':u'洗浴时间点','UseTime':u'用水时长（use_water_time）','GapTime':                    u'总停顿时长（w_pause_time）','w_water':u'总用水量（w_water）','flow_volatility':u'水流量波动（flow_volatility）',                   'water_rate':u'平均水流量（water_rate）','use_water_rate':u'用水/总时长（use_water_rate）','avg_pause_time':                    u'平均停顿时长（avg_pause_time）','pause_volatility':u'停顿时长波动（pause_volatility）'},inplace='True' )

fdf2.index.name=u'事件编号'
fdf2.to_excel('attrConst_results.xlsx')
fdf2


# In[10]:

#-----第*4*步-----接下来进行数据处理和筛选得到“候选洗浴事件，用于接下来的模型构建
# 去掉  用水时长小于100秒
# 去掉 总用水时长小于120秒
# 去掉 一次用水事件中总用水量(纯热水)小于10升
data_filter = fdf2[(fdf2[u'所有使用时间总用水时长（s）']>=120)  & (fdf2[u'总用水量（w_water）']>=10) & (fdf2[u'用水时长（use_water_time）']>=100)]
data_filter.to_excel('data_filter.xlsx')
# data_filter.iloc[:3]
data_filter.head(3)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



