# 代码 8-4
import pandas as pd
import numpy as np
from sklearn.svm import LinearSVR
import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score,\
mean_absolute_error,mean_squared_error,\
median_absolute_error,r2_score
inputfile = '../tmp/new_reg_data_GM11.xls' #灰色预测后保存的路径
data = pd.read_excel(inputfile) #读取数据
feature = ['x1', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x13']
data_train = data.loc[range(1994,2014)].copy()#取2014年前的数据建模
print(data_train.shape)

data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std #数据标准化
x_train = data_train[feature].values #特征数据
y_train = data_train['y'].values #标签数据
x = ((data[feature] - data_mean[feature])  / data_std[feature]).values  #标准差标准化   预测，并还原结果。

linearsvr = LinearSVR().fit(x_train,y_train)  #调用LinearSVR()函数
data[u'y_pred'] = linearsvr.predict(x) * data_std['y'] + data_mean['y']  # y

## SVR预测后保存的结果
outputfile = '../tmp/new_reg_data_GM11_revenue.xls'
data.to_excel(outputfile)
print('真实值与预测值分别为：',data[['y','y_pred']])
ax1=plt.figure(figsize=(5,5)).add_subplot(2,1,1)
print('预测图为：')
data[['y','y_pred']].plot(subplots = True,style=['b-o','r-*'],xticks=data.index[::2]) ##subplots = True两表分开
plt.show()

ax2=plt.figure(figsize=(5,5)).add_subplot(2,1,2)
plt.plot(data['y'])###带有index的值
xticks=data.index[::2]

plt.show()
data=data[:-2]
print('平均绝对误差为：',mean_absolute_error(data['y'].values,data['y_pred'].values))
print('均方误差为：',mean_squared_error(data['y'],data['y_pred']))
print('中值绝对误差为：',median_absolute_error(data['y'],data['y_pred']))
print('可解释方差值为：',explained_variance_score(data['y'],data['y_pred']))
print('R方值为：',r2_score(data['y'],data['y_pred']))