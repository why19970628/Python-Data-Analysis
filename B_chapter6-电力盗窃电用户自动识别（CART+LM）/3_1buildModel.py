
# coding: utf-8

# 1> 数据划分 取20%做测试样本，剩下做训练样本

import pandas as pd
import numpy as np


dt = pd.read_excel('model.xls')
simpler = np.random.permutation(len(dt))
dt = dt.take(simpler) #导入随机函数shuffle，用来打乱数据 注意：不能用shuffle
dt = dt.as_matrix() #将表格转成矩阵格式


p=0.8 #设置训练集的比例
train = dt[:int(len(dt)*p), :] #前80%为训练集
test = dt[int(len(dt)*p):, :] #后20%为测试集


# 2> LM神经网络
#构建LM神经网络模型
from keras.models import Sequential #导入神经网络初始化函数
from keras.layers.core import Dense, Activation #导入神经网络层函数、激活函数

netfile = 'net.model' #构建的神经网络模型存储路径
net = Sequential() # 建立神经网络
net.add(Dense(input_dim = 3, output_dim = 10)) # 添加输入层（3节点）到隐藏层（10节点）的连接
net.add(Activation('relu')) # 隐藏层使用relu激活函数（通过实验确定的relu函数）
net.add(Dense(input_dim = 10, output_dim = 1)) # 添加隐藏层（10节点）到输出层（1节点）的连接
net.add(Activation('sigmoid')) # 输出层使用sigmoid激活函数
net.compile(loss = 'binary_crossentropy', optimizer = 'adam',metrics=None)#编译模型，用adam方法求解

net.fit(train[:,:3], train[:,3], nb_epoch=1000, batch_size=1)# 训练模型，循环1000次
net.save_weights(netfile) #保存模型

predict_result = net.predict_classes(train[:,:3]).reshape(len(train)) #预测类别结果变形
'''
注意：keras使用predict给出预测的概率，使用predict_classes给出预测类别，而且两者预测结果都是nx1维数组
'''
predict_result1 = net.predict(train[:,:3]).reshape(len(train)) #预测概率结果变形


# 2.1> 画混淆矩阵
# 方法1：
# from cm_plot import *# 导入自行编写的混淆矩阵可视化函数 等价于下面的语句
# cm_plot(train[:,3],predict_result).show()#显示混淆矩阵可视化结果

# 方法2：
# 导入相关库，生成混淆矩阵
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
plt.rc('figure',figsize=(5,5))

cm = confusion_matrix(train[:,3],predict_result)
plt.matshow(cm,cmap = plt.cm.Greens) # 背景颜色
plt.colorbar() # 颜色标签

# 内部添加图例标签
for x in range(len(cm)):
    for y in range(len(cm)):
        plt.annotate(cm[x,y], xy = (x,y), horizontalalignment = 'center', verticalalignment = 'center')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.title('LM_train')
plt.savefig('confusionMatrix.jpg')
plt.show()


# 2.2> 计算预测正确率
# 方法1 利用混淆矩阵
from __future__ import division
correctRate = (cm[1,1] + cm[0,0]) / cm.sum()
print correctRate

# # 方法2 逐一比对
# import numpy as np
# train_predict_result = np.column_stack((train, predict_result)) # 合并两个矩阵 列合并(***)
# num = 0
# for i in range(len(train_predict_result)):
#     if train_predict_result[i][3] == train_predict_result[i][4]:
#         num = num+1
# print num/len(train_predict_result)

# 3> 使用CART决策树
from sklearn.tree import DecisionTreeClassifier #导入决策树模型

treefile = 'tree.pkl' #模型输出名字
tree1 = DecisionTreeClassifier() # 建立决策树模型
tree1.fit(train[:,:3], train[:,3]) #训练

#保存模型, 当数据量比较大时，我们更希望把模型持久化的形式保存在磁盘文件中，而不是以字符串（string）的形式保存在内存中 (***)
from sklearn.externals import joblib 
joblib.dump(tree1, treefile)

predict_CartResult = tree1.predict(train[:,:3]) # 使用predict给出预测类别，而且预测结果都是1xN维数组


# 3.1> 画混淆矩阵
# 方法1：
# from cm_plot import *# 导入自行编写的混淆矩阵可视化函数 等价于下面的语句
# cm_plot(train[:,3],predict_CartResult).show()#显示混淆矩阵可视化结果

# 方法2：
# 导入相关库，生成混淆矩阵
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
plt.rc('figure',figsize=(5,5))

cm = confusion_matrix(train[:,3], predict_CartResult)
plt.matshow(cm,cmap = plt.cm.Blues) # 背景颜色
plt.colorbar() # 颜色标签

# 内部添加图例标签
for x in range(len(cm)):
    for y in range(len(cm)):
        plt.annotate(cm[x,y], xy = (x,y), horizontalalignment = 'center', verticalalignment = 'center')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.title('Cart_train')
plt.savefig('confusionMatrix1.jpg')
plt.show()

# 3.2> 计算预测正确率
# 方法1 利用混淆矩阵
from __future__ import division
correctRate = (cm[1,1] + cm[0,0]) / cm.sum()
print correctRate

# # 方法2 逐一比对
# import numpy as np
# train_predict_result = np.column_stack((train, predict_CartResult)) # 合并两个矩阵 列合并(***)
# num = 0
# for i in range(len(train_predict_result)):
#     if train_predict_result[i][3] == train_predict_result[i][4]:
#         num = num+1
# print num/len(train_predict_result)


# 4> 模型评价
# 采用ROC曲线评价方法来测试评估模型分类的性能，一个优秀的分类器应该是尽量靠近左上角的

from sklearn.metrics import roc_curve # 导入ROC曲线
predict_result = net.predict(test[:,:3]).reshape(len(test)) #预测结果变形
fpr, tpr, thresholds = roc_curve(test[:,3], predict_result, pos_label=1)
plt.plot(fpr, tpr, linewidth=2, label='ROC of LM') #作出LM的ROC曲线


fpr1, tpr1, thresholds1 = roc_curve(test[:,3], tree1.predict_proba(test[:,:3])[:,1], pos_label=1)
plt.plot(fpr1, tpr1, linewidth=2, label = 'ROC of CartTree')#做出ROC曲线



plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.xlim(0,1.05)
plt.ylim(0,1.05)
plt.legend(loc=4)
plt.title('comparation of LM and CartTree')
plt.savefig('LOC.jpg')
plt.show()
