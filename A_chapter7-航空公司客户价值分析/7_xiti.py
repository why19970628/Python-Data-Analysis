import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
data=pd.read_csv('./data/test/data.csv',encoding='gb18030')
data=data.iloc[:,1:]
print('原始数据的形状为：',data.shape)
#print(data)
kmeans=KMeans(n_clusters=5)
#data_pred=kmeans.fit_predict(data) ###每个y_pred对应X的一行或一个孩子，聚成5类，类标为0、1、2、3、4
kmeans=kmeans.fit(data)
data_pred=kmeans.predict(data)
print(data_pred)

x = data.iloc[:,0]  #获取第1列的值
print(x)
y = data.iloc[:,1]  #获取第2列的值
print(y)
plt.scatter(x, y, c=data_pred, marker='o')  #c可以为RGB 或者 RGBA二维行数组
plt.title("Kmeans-Basketball Data")  #表示图形的标题为Kmeans-heightweight Data
plt.xlabel("assists_per_minute")  #表示图形x轴的标题
plt.ylabel("points_per_minute")  #表示图形y轴的标题
plt.legend(["Rank"])  #设置右上角图例
plt.show()  #显示图形

