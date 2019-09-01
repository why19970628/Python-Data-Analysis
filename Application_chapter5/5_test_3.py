import pandas as pd
import numpy as np
data=pd.read_csv('./data/test/model.csv',encoding='gbk',sep=',')
print(data.shape)
print(data.memory_usage())
def Standard_Scaler(data):
    data=(data-data.mean())/data.std()
    return data
data1=Standard_Scaler(data['电量趋势下降指标'])
data2=Standard_Scaler(data['线损指标'])
data3=Standard_Scaler(data['告警类指标'])
data4=Standard_Scaler(data['是否窃漏电'])

print(data1.head())
print(data2.head())
a=pd.concat([data1,data2],axis=1)
b=pd.concat([data3,data4],axis=1)
c=pd.concat([a,b],axis=1)
print(c.head(10))