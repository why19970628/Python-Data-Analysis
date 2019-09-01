
# coding: utf-8

# In[2]:


# 3）模型构建
# 目标：判断是否是洗浴事件，是则1，不是则0
# 建立、训练多层神经网络 并完成模型的检验
# 选取”候选洗浴事件“的11个属性作为网络的输入，分别为：洗浴时间点、总用水时长、总停顿时长、平均停顿时长、停顿次数、
# 用水时长、用水时长/总用水时长、总用水量、平均水流量、水流量波动和停顿时长波动
from __future__ import print_function
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# 由于此单元的中间数据处理原书中有问题，所以此处采用书中给的训练数据，和测试数据，旨在测试模型在此数据上的运行
inputfile1 = 'train_neural_network_data.xls' # 训练数据
inputfile2 = 'test_neural_network_data.xls' # 测试数据
testoutputfile = 'test_output_data.xls' #测试数据模型输出文件

data_train = pd.read_excel(inputfile1) # 读入训练数据
data_test = pd.read_excel(inputfile2) # 读入测试数据

data_train.head()


# In[3]:

x_train = data_train.iloc[:,5:17].as_matrix() # 训练样本特征
y_train = data_train.iloc[:,4].as_matrix() # 训练样本标签列
x_test = data_test.iloc[:,5:17].as_matrix() # 测试样本特征
y_test = data_test.iloc[:,4].as_matrix() # 训练样本标签列


# In[4]:


# 训练神经网络时，对神经网络的参数进行寻优，发现含两个隐含层的神经网络训练效果较好
# 其中两个隐层的节点数分别为17和10时训练效果较好

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation

netfile = 'net.model'# 构建的神经网络模型存储路径

model = Sequential() # 建立模型
model.add(Dense(units=17, input_dim=11)) # 添加输入层、隐藏层的连接
model.add(Activation('relu')) # 以relu函数为激活函数
model.add(Dense(units=10, input_dim=17)) # 添加隐藏层、二层隐藏层的连接
model.add(Activation('relu')) # 以relu函数为激活函数
model.add(Dense(units=1, input_dim=10)) # 添加二层隐藏层、输出层的连接
model.add(Activation('sigmoid')) # 以sigmoid函数为激活函数

# 编译模型，损失函数为binary_crossentropy,用adam法求解
model.compile(loss = 'binary_crossentropy', optimizer = 'adam')
model.fit(x_train, y_train, nb_epoch = 1000, batch_size = 1)
model.save_weights(netfile)# 保存模型参数




# In[6]:

predict_result_train = model.predict_classes(x_train).reshape(len(data_train)) #给出预测类别（训练集）
from cm_plot import *
cm_plot(y_train, predict_result_train).show() #显示混淆矩阵可视化结果 看训练结果正确率


# In[11]:

from sklearn.metrics import confusion_matrix
predict_result_test = model.predict_classes(x_test).reshape(len(data_test)) #给出预测类别（测试集）
from cm_plot import *
cm = confusion_matrix(y_test, predict_result_test)
cm_plot(y_test, predict_result_test).show() #显示混淆矩阵可视化结果 看训练结果正确率



# In[13]:

from __future__ import division
correctRate = (cm[1,1] + cm[0,0]) / cm.sum()
correctRate


# In[14]:

r = DataFrame(predict_result_test, columns = [u'预测结果']) # 给出预测类别测试集
# predict_rate = DataFrame(model.predict(x_test), columns = [u'预测正确率']) # 给出预测类别测试集
res = pd.concat([data_test.iloc[:,:5],r], axis=1)#测试集
res.to_excel(testoutputfile)
res


# In[ ]:




# In[ ]:



