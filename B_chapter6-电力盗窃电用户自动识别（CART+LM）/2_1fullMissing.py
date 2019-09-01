
# coding: utf-8


# 数据预处理
# 数据清洗：过滤掉非居民用电数据，过滤节假日的用电数据
# 缺失值处理：补充缺失的数据
# 三种方法：Lagrange插值法和Newton插值法以及Series自带的interpolate
#1、Lagrange插值法和Newton插值法解决实际问题中关于只提供复杂的离散数据的函数求值问题，通过将所考察的函数简单化，构造关于离散数据实际函数f（x）的近似函数P（x），从而可以计算未知点出的函数值，是插值法的基本思路。
#2、实际上Lagrange插值法和Newton插值法是同一种方法的两种变形，其构造拟合函数的思路是相同的，而实验中两个实际问题用两种算法计算出结果是相同的。
#3、实验所得结果精确度并不高，一方面是因为所给数据较少，另一方面也是主要方面在Win32中C++中数据类型double精度只有7位，计算机在进行浮点运算时截断运算会导致误差。实际问题中，测量数据也可能导致误差。
#4、在解决实际问题中，更多是利用精确且高效的计算机求解。所以解决问题时不仅要构造可求解的算法，更重要是构造合理的可以编写成程序由计算机求解的算法，而算法的优化不仅可以节省时间空间，更能得到更为精确有价值的结果。


import pandas as pd
inputfile = 'missing_data.xls' #输入数据
data = pd.read_excel(inputfile, header=None)
# 判断DataFrame中的空值的位置
sij = []
for j in range(len(data.columns)):
    s1 = data[data.columns[j]].isnull()
    for i in range(len(s1)):
        if s1[i]==True:
            sij.append((j,i))
sij

# <1> 拉格朗日插值法
# 自定义列向量插值函数
# s为列向量， n为被插值的位置， k为取前后的数据个数， 默认为5
from scipy.interpolate import lagrange #导入拉格朗日插值函数
data1 = pd.read_excel(inputfile, header=None,names=['A','B','C'])

def plotinterplate_columns(s, n, k=5):
    y = s[list(range(n-k,n) + list(range(n+1, n+1+k)))]
    y = y[y.notnull()]#剔除空值
    return lagrange(y.index, list(y))(n)#向位置n出插值并返回该插值结果

# 逐个判断每列是否需要插值
lagij = []
for i in data1.columns:
    for j in range(len(data1)):
        if (data1[i].isnull())[j]:
            data1[i][j] = plotinterplate_columns(data1[i],j)
            lagij.append((i,j,data1[i][j]))
            
data1


data1.to_csv('lagrange.csv')
from pandas import Series
Series(lagij).to_csv('lagij.csv')

# <2> 牛顿插值法

import matplotlib.pyplot as plt

"""
@brief:   计算n阶差商 f[x0, x1, x2 ... xn] 
@param:   xi   所有插值节点的横坐标集合                                                        o
@param:   fi   所有插值节点的纵坐标集合                                                      /   \
@return:  返回xi的i阶差商(i为xi长度减1)                                                     o     o
@notice:  a. 必须确保xi与fi长度相等                                                        / \   / \
          b. 由于用到了递归，所以留意不要爆栈了.                                           o   o o   o
          c. 递归减递归(每层递归包含两个递归函数), 每层递归次数呈二次幂增长，总次数是一个满二叉树的所有节点数量(所以极易栈溢出)                                                                                     
"""

def get_order_diff_quot(xi = [], fi = []):
    if len(xi) > 2 and len(fi) > 2:
        return (get_order_diff_quot(xi[:len(xi) - 1], fi[:len(fi) - 1]) - get_order_diff_quot(xi[1:len(xi)], fi[1:len(fi)])) / float(xi[0] - xi[-1])
    return (fi[0] - fi[1]) / float(xi[0] - xi[1])
"""

@brief:  获得Wi(x)函数;
         Wi的含义举例 W1 = (x - x0); W2 = (x - x0)(x - x1); W3 = (x - x0)(x - x1)(x - x2)
@param:  i  i阶(i次多项式)
@param:  xi  所有插值节点的横坐标集合
@return: 返回Wi(x)函数
"""

def get_Wi(i = 0, xi = []):
    def Wi(x):
        result = 1.0
        for each in range(i):
            result *= (x - xi[each])
        return result
    return Wi
"""
@brief: 获得牛顿插值函数
"""

def get_Newton_inter(xi = [], fi = []):
    def Newton_inter(x):
        result = fi[0]
        for i in range(2, len(xi)):
            result += (get_order_diff_quot(xi[:i], fi[:i]) * get_Wi(i-1, xi)(x))
        return result
    return Newton_inter
# 自定义列向量插值函数
# s为列向量， n为被插值的位置，k为取前后的数据个数， 默认为5
def plotnewton_columns(s):
    y = s[s.notnull()]#剔除空值
    Nx= get_Newton_inter(y.index, list(y))         #向位置n出插值并返回该插值结果
    return Nx

import pandas as pd
from scipy.optimize import newton #导入牛顿插值函数
inputfile = 'missing_data.xls' #输入数据
data2 = pd.read_excel(inputfile, header=None,names=['A','B','C'])

newij = []
for i in data2.columns:
    Newton = plotnewton_columns(data2[i])
    for j in range(len(data1)):
        if (data2[i].isnull())[j]:
            data2[i][j] = Newton(j)
            newij.append((i,j,data2[i][j]))


data2.to_csv('newton.csv')
from pandas import Series
Series(newij).to_csv('newij.csv')
newij


# <3> Series自带的iterplote
data3=pd.read_excel('missing_data.xls',header=None,names=['A','B','C'])

###利用Pandas中interpolate进行缺失值的补充
data_out = data3.interpolate()

df = data_out - data3.fillna(0)
Serij = []
for i in df.columns:
    for j in range(len(df)):
        if df[i][j] != 0:
            Serij.append((i,j,df[i][j]))


data_out.to_csv('Series.csv')
Series(Serij).to_csv('Serij.csv')
N_L_S = pd.concat([data1,data2,data_out],axis=1)
N_L_S.to_csv('nls.csv')


## 比较三者的填充结果
N = pd.DataFrame(newij,columns = ['col', 'row', 'value'])
L = pd.DataFrame(lagij,columns = ['col', 'row', 'value'])
S = pd.DataFrame(Serij,columns = ['col', 'row', 'value'])
N.set_index(['col','row'],inplace = True)
L.set_index(['col','row'],inplace = True)
S.set_index(['col','row'],inplace = True)


compare = pd.merge(N,pd.merge(L,S,left_index = True, right_index = True),left_index = True, right_index = True)
compare.rename(columns={'value':'Newton','value_x':'lagrange','value_y':'Series'},inplace= True)
compare.ix[:,:] = compare.ix[:,:].applymap(lambda x: '%.3f' % x)  # 一旦执行这个操作，数据类型转成字符串型
# compare['Newton'] = compare['Newton'].astype('float64') # 这一句不能要，否则又恢复原样了
# compare = compare.round(3)# 此句话对科学计数法没起作用
compare.to_csv('compare.csv')
compare

