import pandas as pd
import numpy as np
data1=pd.read_table('./data/test_data/Training_LogInfo.csv',sep=',',encoding='gbk')
data2=pd.read_table('./data/test_data/Training_Userupdate.csv',sep=',',encoding='gbk')
data1['LogInfo3']=pd.to_datetime(data1['LogInfo3'])
data2['UserupdateInfo2']=pd.to_datetime(data2['UserupdateInfo2'])

data1_Group=data1[['Idx','LogInfo3']].groupby(by='Idx')
data2_Group=data2[['Idx','UserupdateInfo2']].groupby(by='Idx')
print(data1_Group['LogInfo3'].size().head())
data1_min=data1['LogInfo3'].min()
data1_max=data1['LogInfo3'].max()
check_time=data1_max-data1_min
print('最早登陆时间',data1_min)
print('最晚登录时间',data1_max)
print('登录时间差',check_time)

data2_min=data2['UserupdateInfo2'].min()
data2_max=data2['UserupdateInfo2'].max()
check_time=data2_max-data2_min
print('最早更新时间',data2_min)
print('最晚更新时间',data2_max)
print('更新时间差',check_time)

print(data1.agg({'LogInfo3':np.size}).index[-1])
print(data2.agg({'UserupdateInfo2':np.size}).index[-1])

