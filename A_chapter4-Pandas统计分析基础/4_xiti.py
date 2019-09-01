import pandas as pd
import numpy as np
mtcars=pd.read_table('./data/test_data/mtcars.csv',sep=',',encoding='gbk')
print(mtcars.memory_usage())
print(mtcars.values[:5,:5])
print(mtcars.ndim)
print(mtcars.shape)
print(mtcars.describe())
data=mtcars.loc[:,['cyl','carb','mpg','hp']]
print(data.head())
data_group=data.groupby(by=['cyl','carb']).mean()
print(data_group)
mpgHp = data.groupby('cyl').mean()
print('不同cyl（汽缸数），carb(化油器)对应的mpg(油耗)和hp(马力)的均值为：\n',mpgHp)

data1=data[['cyl','mpg']].agg([np.mean,np.sum])
print(data1)

