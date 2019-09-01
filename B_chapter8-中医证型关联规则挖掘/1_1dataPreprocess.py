
# coding: utf-8

# 1>  数据预处理 

# 1数据清洗
# 2属性规约
# 3数据变换
# （1）属性构造
# （2）数据离散化

# -*- coding:utf-8 -*-
from __future__ import print_function
import pandas as pd
from pandas import DataFrame,Series
from sklearn.cluster import KMeans#导入K均值聚类算法

datafile = 'data.xls'
resultfile = 'data_processed.xlsx'

typelabel = {u'肝气郁结证型系数':'A',u'热毒蕴结证型系数':'B',u'冲任失调证型系数':'C',u'气血两虚证型系数':'D',u'脾胃虚弱证型系数':'E',u'肝肾阴虚证型系数':'F'}

k = 4 #需要进行的聚类类别数

#读取文件进行聚类分析
data = pd.read_excel(datafile)
keys = list(typelabel.keys())
result = DataFrame()

for i in range(len(keys)):
    #调用k-means算法 进行聚类
    print(u'正在进行%s的聚类' % keys[i])
    kmodel = KMeans(n_clusters = k, n_jobs = 4)  # n_job是线程数，根据自己电脑本身来调节
    kmodel.fit(data[[keys[i]]].as_matrix())# 训练模型
#     kmodel.fit(data[[keys[i]]]) # 不转成矩阵形式结果一样
#KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
#     n_clusters=4, n_init=10, n_jobs=4, precompute_distances='auto',
#     random_state=None, tol=0.0001, verbose=0)
    
    r1 = DataFrame(kmodel.cluster_centers_, columns = [typelabel[keys[i]]]) # 聚类中心
    r2 = Series(kmodel.labels_).value_counts() #分类统计
    r2 = DataFrame(r2,columns = [typelabel[keys[i]]+'n'])# 转成DataFrame格式，记录各个类别的数目
    r = pd.concat([r1,r2], axis=1).sort_values(typelabel[keys[i]])
    r.index = range(1,5)
    r[typelabel[keys[i]]] = pd.rolling_mean(r[typelabel[keys[i]]],2) # rolling_mean用来计算相邻两列的均值，以此作为边界点
    r[typelabel[keys[i]]][1] = 0.0 # 将原来的聚类中心改成边界点
    result = result.append(r.T)
result = result.sort_index() # 以index排序，以ABCDEF排序
result.to_excel(resultfile)
    
print (result)
# '''
#         1           2           3           4
# A     0.0    0.178698    0.257724    0.351843
# An  240.0  356.000000  281.000000   53.000000
# B     0.0    0.150766    0.296631    0.489705
# Bn  325.0  396.000000  180.000000   29.000000
# C     0.0    0.202149    0.289061    0.423537
# Cn  297.0  394.000000  204.000000   35.000000
# D     0.0    0.172049    0.251583    0.359353
# Dn  283.0  375.000000  228.000000   44.000000
# E     0.0    0.152698    0.257762    0.375661
# En  273.0  319.000000  244.000000   94.000000
# F     0.0    0.179143    0.261386    0.354643
# Fn  200.0  237.000000  265.000000  228.000000
# '''

# 2>划分原始数据中的类别
import pandas as pd
data.head()

# 将分类后数据进行处理
data_cut = DataFrame(columns = data.columns[:6])
types = ['A','B','C','D','E','F']
num = ['1','2','3','4']
for i in range(len(data_cut.columns)):
    value = list(data.iloc[:,i])
    bins = list(result[(2*i):(2*i+1)].values[0])
    bins.append(1)
    names = [str(x)+str(y) for x in types for y in num]
    group_names = names[4*i:4*(i+1)]
    cats = pd.cut(value,bins,labels=group_names,right=False)
    data_cut.iloc[:,i] = cats
data_cut.to_excel('apriori.xlsx')
data_cut.head()

