
# coding: utf-8

# In[1]:


# 数据预处理
#---* 1 *---数据清洗
import pandas as pd
import numpy as np
from pandas import DataFrame,Series

inputfile1 = 'discdata.xls'
data = pd.read_excel(inputfile1)
data.head()


# In[2]:

# 一般情况下默认磁盘容量是定值，所以需要剔除磁盘容量重复的数据
data.drop_duplicates(data.columns[:-1],inplace=True)
data.to_excel('dataCleaned.xlsx')
data.head()


# In[3]:

#---* 2 *---属性构造 
# 思路：由于每台服务器上的这三个属性值一直不变：NAME、TARGET_ID、ENTITY，将这三个属性值合并
inputfile2 = 'dataCleaned.xlsx'
data = pd.read_excel(inputfile2)


# In[4]:

# 教材上方法一：
df = data[data['TARGET_ID'] == 184].copy() # 只选取TARGET_ID为184的数据
df_group = df.groupby('COLLECTTIME') # 以时间分组得到一个GroupBy对象

#定义属性变换函数
def attr_trans(x):
    result = Series(index = ['SYS_NAME','CWXT_DB:184:C:\\','CWXT_DB:184:D:\\','COLLECTTIME'])
    result['SYS_NAME'] = x['SYS_NAME'].iloc[0]
    result['COLLECTTIME'] = x['COLLECTTIME'].iloc[0]
    result['CWXT_DB:184:C:\\'] = x['VALUE'].iloc[0]
    result['CWXT_DB:184:D:\\'] = x['VALUE'].iloc[1]
    return result 
    
data_attr_constr = df_group.apply(attr_trans)# 逐组处理
data_attr_constr.to_excel('attrsConstruction.xlsx',index=False)
data_attr_constr


# In[5]:

#方法二，死方法，没有方法一灵活
df_g = df.groupby('COLLECTTIME').size()
indexpre = df_g.index
data_processed = DataFrame([],index = indexpre, columns=['SYS_NAME','CWXT_DB:184:C:\\','CWXT_DB:184:D:\\'])
data_processed['SYS_NAME'] =  u'财务管理系统'
data_processed['CWXT_DB:184:C:\\'] = df['VALUE'][df['ENTITY']=='C:\\'].values
data_processed['CWXT_DB:184:D:\\'] = df['VALUE'][df['ENTITY']=='D:\\'].values
data_processed.head()


# In[ ]:




# In[ ]:




# In[ ]:



