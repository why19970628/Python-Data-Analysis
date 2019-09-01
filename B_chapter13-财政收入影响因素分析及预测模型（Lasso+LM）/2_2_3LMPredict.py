
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
inputfile1 = '2_2_2_1greyPredict.xlsx'
data = pd.read_excel(inputfile1)
data # 1994到2013年间的各个影响因素的数据
feature = ['x1', 'x3',  'x5'] # 特征所在列

# 准备模型数据
data_train = data.loc[range(1999,2014)].copy() # 取2014年前的数据建模
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train-data_mean)/data_std # 均值标准化
x_train = data_train[feature].as_matrix() # 特征数据
y_train = data_train['y'].as_matrix() # 标签数据


# In[2]:

# 利用神经网络建模
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import time 
start = time.clock()

#输入层为３个节点，隐藏层６个节点
model = Sequential() # 建立模型
model.add(Dense(output_dim =6, input_dim=3)) # 添加输入层、隐藏层节点
model.add(Activation('relu')) # 使用relu作为激活函数，可以大幅度提高准确率
model.add(Dense(units=1, input_dim=6)) # 添加输出层节点
model.compile(loss = 'mean_squared_error', optimizer = 'adam') # 编译模型
model.fit(x_train, y_train, nb_epoch = 3000, batch_size=16) #训练模型，学习一千次
end = time.clock()
usetime = end-start
print '训练该模型耗时'+ str(usetime) +'s!'
model.save_weights('2_net.model') # 将该模型存储


# In[3]:

# 预测并还原结果
x = ((data[feature] - data_mean[feature])/data_std[feature]).as_matrix()
data[u'y_pred'] = model.predict(x) * data_std['y'] + data_mean['y']
#保存的表名命名格式为“2_2_3_1k此表功能名称”，是此小节生成的第1张表格，功能为revenue：增值税预测结果
data.to_excel('2_2_3_1zengzhi.xlsx')


import matplotlib.pyplot as plt # 画出预测结果图
plt.rc('figure',figsize=(7,7))
p = data[['y','y_pred']].plot(subplots = True, style=['b-o', 'r-*'])
plt.savefig('zengzhi.jpg')
plt.show()


# In[4]:

data


# In[ ]:



