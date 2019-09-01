# 代码 3-12
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
data = np.load('./data/国民经济核算季度数据.npz')
name = data['columns']## 提取其中的columns数组，视为数据的标签
values = data['values']## 提取其中的values数组，数据的存在位置
print(name)
print(values)
plt.figure(figsize=(6,5))## 设置画布
plt.bar(range(3),values[-1,3:6],width = 0.5)## 绘制散点图
plt.xlabel('产业')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
label = ['第一产业','第二产业','第三产业']## 刻度标签
plt.xticks(range(3),label)
plt.title('2017年第一季度各产业国民生产总值直方图')## 添加图表标题
plt.savefig('./tmp/2017年第一季度各产业国民生产总值直方图.png')
plt.show()

# 代码 3-13
plt.figure(figsize=(6,6))## 将画布设定为正方形，则绘制的饼图是正圆
label= ['第一产业','第二产业','第三产业']## 定义饼状图的标签，标签是列表
explode = [0.01,0.01,0.01]## 设定各项离心n个半径
plt.pie(values[-1,3:6],explode=explode,labels=label,
        autopct='%1.1f%%')## 绘制饼图
plt.title('2017年第一季度各产业国民生产总值饼图')
plt.savefig('./tmp/2017年第一季度各产业生产总值占比饼图')
plt.show()

# 代码 3-14
label= ['第一产业','第二产业','第三产业']## 定义标签
gdp = (list(values[:,3]),list(values[:,4]),list(values[:,5]))
plt.figure(figsize=(6,4))
plt.boxplot(gdp,notch=True,labels = label, meanline=True)
plt.title('2000-2017各产业国民生产总值箱线图')
plt.savefig('./tmp/2000-2017各产业国民生产总值箱线图.png')
plt.show()