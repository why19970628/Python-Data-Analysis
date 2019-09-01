
# coding: utf-8

#　10-fold cross-validation 十折交叉验证方法

# 1> 数据划分 取20%做测试样本，剩下做训练样本

import pandas as pd
import numpy as np


dt = pd.read_excel('model.xls')
simpler = np.random.permutation(len(dt))
dt = dt.take(simpler) #导入随机函数shuffle，用来打乱数据 注意：不能用shuffle
dt = dt.as_matrix() #将表格转成矩阵格式


# 2> 十折决策树算法
from sklearn.tree import DecisionTreeClassifier #导入决策树模型
from __future__ import division
from sklearn.metrics import confusion_matrix
p = 0.1 #设置训练集的比例
N = 1/p
correctRate = []
for i in range(int(N)):
    demotest = dt[int(len(dt)*(p*i)):int(len(dt)*(p*(i+1))), :]
    demotrain = np.row_stack((dt[:int(len(dt)*(p*i)), :], dt[int(len(dt)*(p*(i+1))):, :]))
    
    tree = DecisionTreeClassifier() # 建立决策树模型
    tree.fit(demotrain[:,:3], demotrain[:,3]) #训练模型
    
    predict_CartResult = tree.predict(demotest[:,:3]) # 测试模型
    cm = confusion_matrix(demotest[:,3], predict_CartResult)
    cRate = (cm[1,1] + cm[0,0]) / cm.sum()
    correctRate.append(cRate)
print sum(correctRate)/len(correctRate) # 求这是个正确率的均值 #predict_classes（随数据集的组合而变化）


#  3> 十折LM神经网络
# #构建LM神经网络模型
from keras.models import Sequential #导入神经网络初始化函数
from keras.layers.core import Dense, Activation #导入神经网络层函数、激活函数
from __future__ import division
from sklearn.metrics import confusion_matrix

p = 0.1 #设置训练集的比例
N = 1/p
correctRateLM = []
for i in range(int(N)):
    demotest = dt[int(len(dt)*(p*i)):int(len(dt)*(p*(i+1))), :]
    demotrain = np.row_stack((dt[:int(len(dt)*(p*i)), :], dt[int(len(dt)*(p*(i+1))):, :]))
    
    net = Sequential() # 建立神经网络
    net.add(Dense(input_dim = 3, output_dim = 10)) # 添加输入层（3节点）到隐藏层（10节点）的连接
    net.add(Activation('relu')) # 隐藏层使用relu激活函数（通过实验确定的relu函数）
    net.add(Dense(input_dim = 10, output_dim = 1)) # 添加隐藏层（10节点）到输出层（1节点）的连接
    net.add(Activation('sigmoid')) # 输出层使用sigmoid激活函数
    net.compile(loss = 'binary_crossentropy', optimizer = 'adam',metrics=None)#编译模型，用adam方法求解
    net.fit(demotrain[:,:3], demotrain[:,3], nb_epoch=1000, batch_size=1)# 训练模型，循环1000次
    
    predict_result = net.predict_classes(demotest[:,:3]).reshape(len(demotest)) #预测结果变形,预测结果都是nx1维数组
    cm = confusion_matrix(demotest[:,3],predict_result)
    cRate = (cm[1,1] + cm[0,0]) / cm.sum()
    correctRateLM.append(cRate)
print sum(correctRateLM)/len(correctRateLM) # 求这是个正确率的均值
