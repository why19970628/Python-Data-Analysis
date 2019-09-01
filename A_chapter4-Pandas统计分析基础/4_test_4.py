import pandas as pd
import numpy as np
data1=pd.read_table('./data/test_data/Training_LogInfo.csv',sep=',',encoding='gbk')
data2=pd.read_table('./data/test_data/Training_Userupdate.csv',sep=',',encoding='gbk')

data1_Pivot=pd.pivot_table(data1[['Idx','LogInfo3','LogInfo1']],index='LogInfo3',values='Idx')
print(data1_Pivot.head())

data2_Pivot=pd.pivot_table(data2[['Idx','UserupdateInfo2','UserupdateInfo1']],index='UserupdateInfo1',values='Idx')
print(data2_Pivot.head())

#Crosstab_data1=pd.crosstab(index=data1['LogInfo3'],values=data1['Idx'],margins=True,columns=data1['LogInfo1'])
#print(Crosstab_data1.head())