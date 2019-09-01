
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
inputfile1 = 'data1.csv'
data = pd.read_csv(inputfile1)
data # 1994到2013年间的各个影响因素的数据


# In[2]:

# ---------------* 1_1summaryMeasure *---------------
# 概括性分析描述性统计
r = [data.min(), data.max(), data.mean(), data.std()] #统计最小、最大、平均、标准差
r = pd.DataFrame(r, index= ['Min', 'Max', 'Mean', 'Std']).T #计算相关系数矩阵
result = np.round(r, 2) # 保留两位小数  （***）
# np.round(data.describe().T[['min', 'max', 'mean', 'std']],2) # 等价于上面数据探索
#保存的表名命名格式为“1_k此表功能名称”，是此小节生成的第1张表格，功能为summaryMeasure：概括性分析描述性统计
result.to_excel('1_1summaryMeasure.xlsx')
result


# In[3]:

# ---------------* 1_2relatedAnalysis *---------------

# 计算各个变量之间的皮尔森系数'pearson'/ 'kendall'/ 'spearman'
result1 = np.round(data.corr(method='pearson'), 2)
#保存的表名命名格式为“1_k此表功能名称”，是此小节生成的第2张表格，功能为relatedAnalysis：相关性分析
result1.to_csv("1_2relatedAnalysis.csv")
result1


# In[4]:

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
get_ipython().magic(u'matplotlib inline')


# In[6]:

corrmat = data.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True);


# In[ ]:




# In[ ]:



