import pandas as pd
data=pd.read_table('./data/test_data/Training_LogInfo.csv',sep=',',encoding='gbk')
print(data.values)
print(data.ndim)
print(data.shape)
print(data.memory_usage())
print('data desc',data.describe())
#print('data.desc',Training_LogInfo.describe())
print(data.loc[:,'Idx'].describe())

def dropNulldata(data):
    before_len = data.shape[1]
    dataIsNull = data.describe().loc['count'] == 0
    for i in range(len(dataIsNull)):
        if dataIsNull[i]:
            data.drop(dataIsNull[i],axis=1,inplace=True)

    dataIsZero=data.describe().loc['std']==0
    for i in range(len(dataIsZero)):
        if dataIsZero[i]:
            data.drop(dataIsZero[i],axis=1,inplace=True)
    after=data.shape[1]
    print('删除的数列为:',before_len-after)
    print('删除后的形状为:',data.shape)
dropNulldata(data)

