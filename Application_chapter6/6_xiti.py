from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
iris=load_iris()
iris_data=iris['data']
iris_target=iris['target']
#print(iris_data)
(iris_data_train,iris_data_test,iris_target_train,iris_target_test)=train_test_split(iris_data,iris_target)
pac_model=PCA(n_components=3).fit(iris_data_train)
iris_data_trainPca=pac_model.transform(iris_data_train)
iris_data_testPca=pac_model.transform(iris_data_test)
print(iris_data_train.shape)
print(iris_data_trainPca.shape)

from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import roc_curve  ### ROC只能针对二分类问题
svm=SVC().fit(iris_data_trainPca,iris_target_train)
iris_target_testPred=svm.predict(iris_data_testPca)
print(iris_target_testPred[:20])
true=np.sum(iris_target_testPred==iris_target_test)
print('对的结果数目',true)
print('错的结果数目',iris_target_test.shape[0]-true)

from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
print('SVM预测分类结果分类报告','\n',classification_report(iris_target_test,iris_target_testPred))