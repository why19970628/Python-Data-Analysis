import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
wine=pd.read_csv('./data/test/wine.csv',sep=',')
wine_quality=pd.read_csv('./data/test/winequality.csv',sep=';')

wine_data=wine.iloc[:,1:]
wine_target=wine.iloc[:,0]
wine_train,wine_test,wine_target,wine_target_test=train_test_split(wine_data,wine_target)
Scaler=MinMaxScaler().fit(wine_train)
wine_trainScaler=Scaler.transform(wine_train)
wine_testScaler=Scaler.transform(wine_test)

pca_model=PCA(n_components=5).fit(wine_trainScaler)
wine_train_Pca=pca_model.transform(wine_trainScaler)
wine_test_Pca=pca_model.transform(wine_testScaler)
print('wine_train_Pca降维前的形状',wine_train.shape,'\nwine_train_Pca降维后的形状',wine_train_Pca.shape)
print('wine_test_Pca降维前的形状',wine_test.shape,'\nine_test_Pca降维后的形状',wine_test_Pca.shape)


print(wine_quality.shape,wine_quality.memory_usage())


wine_quality_data=wine_quality.iloc[:,:-2]
wine_quality_target=wine_quality.iloc[:,-1]
wine_quality_train,wine_quality_test,wine_quality_target,wine_quality_target_test=train_test_split(
    wine_quality_data,wine_quality_target)
#print(wine_quality_train.shape,wine_quality_test.shape)

Scaler=StandardScaler().fit(wine_quality_train)
wine_quality_trainScaler=Scaler.transform(wine_quality_train)
wine_quality_testScaler=Scaler.transform(wine_quality_test)

pca_model=PCA(n_components=5).fit(wine_quality_trainScaler)
wine_quality_train_Pca=pca_model.transform(wine_quality_trainScaler)
wine_quality_test_Pca=pca_model.transform(wine_quality_testScaler)
print(wine_quality_train_Pca.shape,wine_quality_test_Pca.shape)


#####  test2
from sklearn.cluster import KMeans
from sklearn.metrics import fowlkes_mallows_score
from sklearn.metrics import calinski_harabaz_score
import matplotlib.pyplot as plt
kmeans=KMeans(n_clusters=3,random_state=42).fit(wine_train_Pca)
score_line=[]
for i in range(2,11):
    kmeans = KMeans(n_clusters=i, random_state=42).fit(wine_train_Pca)
    score=fowlkes_mallows_score(wine_target,kmeans.labels_)
    print('wine数据%d类FMI指数为：%f' %(i,score))
    score_line.append(score)
plt.figure(figsize=(10,6))
plt.plot(range(2,11),score_line,linewidth=1.5,linestyle='-')
plt.savefig('./tmp/test3_wine_FMI评价折线图.png')
plt.show()

########  test3
from sklearn.svm import SVC
from sklearn.metrics import  classification_report
svm=SVC().fit(wine_trainScaler,wine_target)
wine_target_test_pred=svm.predict(wine_test)
print(wine_target_test_pred[:30])
print(classification_report(wine_target_test,wine_target_test_pred))


#####   test4
from sklearn.linear_model import  LinearRegression
from matplotlib import rcParams
from sklearn.metrics import explained_variance_score,mean_absolute_error,mean_squared_error,median_absolute_error,r2_score
clf=LinearRegression().fit(wine_quality_train,wine_quality_target) ##线性回归模型
###wine_quality_train,wine_quality_test,wine_quality_target,wine_quality_target_test
print(clf)
wine_quality_target_test_pred=clf.predict(wine_quality_test)
print(wine_quality_target_test_pred[:20])
rcParams['font.sans-serif'] = 'SimHei'
fig = plt.figure(figsize=(10,6)) ##设定空白画布，并制定大小
##用不同的颜色表示不同数据
plt.plot(range(wine_quality_test.shape[0]),wine_quality_target_test,color="blue", linewidth=1.5, linestyle="-")
plt.plot(range(wine_quality_test.shape[0]),wine_quality_target_test_pred,color="red", linewidth=1.5, linestyle="-.")
plt.legend(['真实值','预测值'])
plt.savefig('./tmp/wine_quality_target线性回归预测.png')
plt.show() ##显示图片

print('wine_quality数据线性回归模型的平均误差为',mean_absolute_error(wine_quality_target_test,wine_quality_target_test_pred))
print('wine_quality数据线性回归模型的均方误差',mean_squared_error(wine_quality_target_test,wine_quality_target_test_pred))
print('wine_quality数据线性回归模型的中值绝对误差为',median_absolute_error(wine_quality_target_test,wine_quality_target_test_pred))
print('wine_quality数据线性回归模型的可解释方差值为 ',explained_variance_score(wine_quality_target_test,wine_quality_target_test_pred))
print('wine_quality数据线性回归模型的R²值',r2_score(wine_quality_target_test,wine_quality_target_test_pred))


from sklearn.ensemble import GradientBoostingRegressor
GBR_wine_quality=GradientBoostingRegressor().fit(wine_quality_train,wine_quality_target)#梯度回归
wine_quality_test_pred=GBR_wine_quality.predict(wine_quality_test)
print('\n',wine_quality_test_pred[:20])
print('wine数据梯度提升回归模型的平均误差为',mean_absolute_error(wine_quality_target_test,wine_quality_test_pred))
print('wine数据梯度提升回归模型的均方误差',mean_squared_error(wine_quality_target_test,wine_quality_test_pred))
print('wine数据梯度提升回归模型的中值绝对误差为',median_absolute_error(wine_quality_target_test,wine_quality_test_pred))
print('wine数据梯度提升回归模型的可解释方差值为',explained_variance_score(wine_quality_target_test,wine_quality_test_pred))
print('wine数据梯度提升回归模型的R²值',r2_score(wine_quality_target_test,wine_quality_test_pred))






