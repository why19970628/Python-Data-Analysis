import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
data = np.load('./data/国民经济核算季度数据.npz')

name = data['columns'] ## 提取其中的columns数组，视为数据的标签
values = data['values']## 提取其中的values数组，数据的存在位置
print(data['columns'])
print(data['values'])

# 代码 3-7
plt.figure(figsize=(8,7))## 设置画布
## 绘制折线图
plt.plot(values[:,0],values[:,2],color = 'r',linestyle = '--')
plt.xlabel('年份')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(0,70,4),values[range(0,70,4),1],rotation=45)
plt.title('2000-2017年季度生产总值折线图')## 添加图表标题
plt.savefig('./tmp/2000-2017年季度生产总值折线图.png')
plt.show()

# 代码 3-8
plt.figure(figsize=(8,7))## 设置画布
plt.plot(values[:,0],values[:,2],color = 'r',linestyle = '--',marker = 'o')## 绘制折线图
plt.xlabel('年份')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(0,70,4),values[range(0,70,4),1],rotation=45)
plt.title('2000-2017年季度生产总值点线图')## 添加图表标题
plt.savefig('./tmp/2000-2017年季度生产总值点线图.png')
plt.show()

# 代码 3-9
plt.figure(figsize=(8,7))## 设置画布
plt.plot(values[:,0],values[:,3],'bs-',
       values[:,0],values[:,4],'ro-.',
       values[:,0],values[:,5],'gH--')## 绘制折线图
plt.xlabel('年份')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(0,70,4),values[range(0,70,4),1],rotation=45)
plt.title('2000-2017年各产业季度生产总值折线图')## 添加图表标题
plt.legend(['第一产业','第二产业','第三产业'])
plt.savefig('./tmp/2000-2017年季度各产业生产总值折线散点图.png')
plt.show()
