import numpy as np
import pandas as pd
data=pd.read_csv('./data/test/credit_card.csv',encoding='gb18030')
print('原始数据的形状为：',data.shape)
print(data.memory_usage())
index1=data['逾期'] !=1
index2=data['呆账'] !=1
index3=data['强制停卡记录'] !=1
index4=data['退票'] !=1
index5=data['拒往记录'] !=1
index6=data['瑕疵户'] !=2
data=data[(index1 | index2 | index3 | index4 | index5 | index6)]
print('1:',data.shape)
index7=data['呆账'] | data['强制停卡记录'] | data['退票'] !=1
index8=data['拒往记录'] !=2
data=data[index7 | index8]
print('2:',data.shape)
index9=data['频率'] !=5
index10=data['月刷卡额'] ==1
data=data[index9 | index10]
print('3:',data.shape)

####  test2
data_xingwei=data[['瑕疵户','逾期','呆账','强制停卡记录','退票','拒往记录']]
data_jingji=data[['借款余额','个人月收入','个人月开销','月刷卡额']]
data_shouru=data[['职业','年龄','住家']]

from sklearn.preprocessing import StandardScaler
data_xingwei=StandardScaler().fit_transform(data_xingwei)
data_jingji=StandardScaler().fit_transform(data_jingji)
data_shouru=StandardScaler().fit_transform(data_shouru)
#print('标准化后LRFMC五个特征为：\n',data_xingwei[:5,:])

from sklearn.cluster import KMeans
k = 5 ## 确定聚类中心数
#构建模型
kmeans_model = KMeans(n_clusters = k,n_jobs=4,random_state=123)
fit_kmeans = kmeans_model.fit(data_xingwei)   #模型训练
print(kmeans_model.cluster_centers_) #查看聚类中心
print(kmeans_model.labels_)
r1=pd.Series(kmeans_model.labels_).value_counts() #每类的数目
print(r1)

fit_kmeans = kmeans_model.fit(data_jingji)   #模型训练
print(kmeans_model.cluster_centers_) #查看聚类中心
print(kmeans_model.labels_)
r1=pd.Series(kmeans_model.labels_).value_counts() #每类的数目
print(r1)

fit_kmeans = kmeans_model.fit(data_shouru)   #模型训练
print(kmeans_model.cluster_centers_) #查看聚类中心
print(kmeans_model.labels_)
r1=pd.Series(kmeans_model.labels_).value_counts() #每类的数目
print(r1)







