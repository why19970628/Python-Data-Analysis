import pandas as pd
data1=pd.read_table('./data/test_data/Training_Master.csv',sep=',',encoding='gbk')
data2=pd.read_table('./data/test_data/Training_Userupdate.csv',sep=',',encoding='gbk')
print(data1['ListingInfo'].tail())
print(data1.ndim)
print(data1.shape)
print(data1.memory_usage())
print(data1['ListingInfo'].dtypes)
data1['ListingInfo']=pd.to_datetime(data1['ListingInfo'])
#print(data1['ListingInfo'].dtypes)
print(data1['ListingInfo'].head())
year1=[i.year for i in data1['ListingInfo']]
s=[i.minute for i in data1['ListingInfo']]
month1=[i.month for i in data1['ListingInfo']]
week1=[i.week for i in data1['ListingInfo']]
print(year1[:5],month1[:5],week1[:5])

data2['ListingInfo1']=pd.to_datetime(data2['ListingInfo1'])
print(data2['ListingInfo1'].head())
year1=[i.year for i in data2['ListingInfo1']]
month1=[i.month for i in data2['ListingInfo1']]
week1=[i.week for i in data2['ListingInfo1']]
print(year1[:5],month1[:5],week1[:5])

time_jian=data1['ListingInfo']-data2['ListingInfo1']
print('时间差为',time_jian.head())



