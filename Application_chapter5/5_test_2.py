import pandas as pd
import numpy as np
data1=pd.read_csv('./data/test/ele_loss.csv',encoding='gbk',sep=',')
data2=pd.read_csv('./data/test/alarm.csv',encoding='gbk',sep=',')
data1['ID']=data1['ID'].astype('str')
data2['ID']=data2['ID'].astype('str')
data1['date']=data1['date'].astype('str')
data2['date']=data2['date'].astype('str')
print(data1.shape,data2.shape)
new_data=pd.merge(data1,data2,left_on=['ID','date'],right_on=['ID','date'],how='inner',sort='True')
print(new_data.shape)
print(new_data.values)