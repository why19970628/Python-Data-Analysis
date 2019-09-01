import numpy as np
import pandas as pd
from  sklearn.cluster import KMeans
airline_scale = np.load('./tmp/airline_scale.npz')['arr_0']
#print(airline_scale.files)
k = 5 ## 确定聚类中心数
#构建模型
kmeans_model = KMeans(n_clusters = k,n_jobs=4,random_state=123)
fit_kmeans = kmeans_model.fit(airline_scale)   #模型训练
print(kmeans_model.cluster_centers_) #查看聚类中心
print(kmeans_model.labels_)
r1=pd.Series(kmeans_model.labels_).value_counts() #每类的数目
print(r1)