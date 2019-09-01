import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
inputfile = '../data/test/income_tax.csv' ## 输入的数据文件
data = pd.read_csv(inputfile) ## 读取数据票
print(data.shape)
print(np.round(data.corr(method='pearson'),2))
####  test2
lasso = Lasso(1000)  #调用Lasso()函数，设置λ的值为1000
lasso.fit(data.iloc[:,:-1],data['y'])
print('相关系数为：',np.round(lasso.coef_,5))  #输出结果，保留五位小数

print('相关系数非零个数为：',np.sum(lasso.coef_ != 0))
print(lasso.coef_.shape)
#print(data.columns[1:-1])

mask=lasso.coef_ != 0
print(mask)
Lasso_income_tax=data.iloc[:, mask]
print(Lasso_income_tax)
outfile = '../data/test/income_tax_Lasso.csv'
#outfile='D:/软件（学习）/Python/数据分析与挖掘/chapter8\data/test'
Lasso_income_tax.to_csv(outfile,index=False)



import numpy as np
import pandas as pd
from GM11 import GM11   ## 引入自编的灰色预测函数
inputfile1 = '../data/test/income_tax_Lasso.csv' ##输入新的非零数据文件
inputfile = '../data/test/income_tax.csv' ## 输入的数据文件
new_reg_data = pd.read_csv(inputfile1) ## 读取经过特征选择后的数据
data = pd.read_csv(inputfile) ##读取总的数据

new_reg_data.index = range(2004, 2016)
new_reg_data.loc[2016] = None
new_reg_data.loc[2017] = None
l=data.columns[1:-1]
print(new_reg_data.shape,len(new_reg_data),l)
for i in l:
  f = GM11(new_reg_data.loc[range(2004, 2016),i].values)[0]
  new_reg_data.loc[2016, i] = f(len(new_reg_data) - 1)  # 2014年预测结果
  new_reg_data.loc[2017, i] = f(len(new_reg_data))  ##2015年预测结果
  new_reg_data[i] = new_reg_data[i].round(2)  ## 保留两位小数
outputfile = '../data/test/income_tax_test.xls'  ## 灰色预测后保存的路径
y = list(data['y'].values)  ## 提取财政收入列，合并至新数据框中
y.extend([np.nan, np.nan])
new_reg_data['y'] = y
new_reg_data.drop(labels='year',axis=1,inplace=True)
new_reg_data.to_excel(outputfile)  ## 结果输出
print('预测结果为：', new_reg_data.loc[2016:2017,:])  ##预测结果展示

