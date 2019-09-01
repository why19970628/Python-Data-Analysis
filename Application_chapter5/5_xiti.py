import pandas as pd
import numpy as np
data=[200,300,400,600,1000]
Ser1 = pd.Series(data)#变成一维矩阵.
print(data,Ser1)
# 最小-最大规范化
def MinMaxScaler(data):
    scaler = (data-data.min())/(data.max()-data.min())
    return scaler
print(MinMaxScaler(Ser1))


# 标准差标准化
def StandardScaler(data):
    data=(data-data.mean())/data.std()
    return data
print(StandardScaler(Ser1))

# 小数定标规范化
def DecimalScaler(data):
    data=data/10**np.ceil(np.log10(data.abs().max()))
    return data
print(DecimalScaler(Ser1))


########   2
price = np.array([5,10,11,13,15,35,50,55,72,92,204,215])
price1=pd.Series(price)
print(pd.cut(price1,3))
def SameRateCut(data,k):
    w=data.quantile(np.arange(0,1+1.0/k,1.0/k))
    print('w=\n',w)
    data=pd.cut(data,w)
    return data
result=SameRateCut(price1,3)   ##菜品售价等频法离散化
print('等频法离散化后各个类别数目分布状况为：','\n',result)



#########  3
def PreProcessing(data):
    data.drop_duplicate(inplace = True)
    data.fillna(data.median(),inplace = True)
    return(data)