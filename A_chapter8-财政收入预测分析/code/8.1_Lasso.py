# 代码 8-1
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
inputfile = '../data/data.csv' ## 输入的数据文件
data = pd.read_csv(inputfile) ## 读取数据
## 保留两位小数
#print('相关系数矩阵为：',np.round(data.corr(method = 'pearson'), 2))##返回四舍五入值 ##person 皮尔森相关系数
#每一列数据进行相关系数的计算，其结果等同于取出每列数据采用 np.corrcoef 计算

lasso = Lasso(1000)  #调用Lasso()函数，设置λ的值为1000
lasso.fit(data.iloc[:,0:13],data['y'])
print('相关系数为：',np.round(lasso.coef_,5))  #输出结果，保留五位小数

## 计算相关系数非零的个数
print('相关系数非零个数为：',np.sum(lasso.coef_ != 0))
print(lasso.coef_.shape)
mask = lasso.coef_ != 0  #返回一个相关系数是否为零的布尔数组
print('相关系数是否为零：',mask)

outputfile = '../tmp/new_reg_data.csv'  #输出的数据文件
new_reg_data = data.iloc[:, mask]  #返回相关系数非零的数据
new_reg_data.to_csv(outputfile)  #存储数据
print('输出数据的维度为：',new_reg_data.shape)  #查看输出数据的维度



import numpy as np
import pandas as pd
from GM11 import GM11   ## 引入自编的灰色预测函数
inputfile = '../tmp/new_reg_data.csv' ##输入的数据文件
inputfile1 = '../data/data.csv' ## 输入的数据文件
new_reg_data = pd.read_csv(inputfile) ## 读取经过特征选择后的数据
data = pd.read_csv(inputfile1) ##读取总的数据
new_reg_data.index = range(1994, 2014)
new_reg_data.loc[2014] = None
new_reg_data.loc[2015] = None
l = ['x1', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x13']
for i in l:
  f = GM11(new_reg_data.loc[range(1994, 2014),i].values)[0]
  new_reg_data.loc[2014, i] = f(len(new_reg_data) - 1)  # 2014年预测结果
  new_reg_data.loc[2015, i] = f(len(new_reg_data))  ##2015年预测结果
  new_reg_data[i] = new_reg_data[i].round(2)  ## 保留两位小数
outputfile = '../tmp/new_reg_data_GM11.xls'  ## 灰色预测后保存的路径
y = list(data['y'].values)  ## 提取财政收入列，合并至新数据框中
y.extend([np.nan, np.nan])
new_reg_data['y'] = y
new_reg_data.to_excel(outputfile)  ## 结果输出
print('预测结果为：', new_reg_data.loc[2014:2015, :])  ##预测结果展示
