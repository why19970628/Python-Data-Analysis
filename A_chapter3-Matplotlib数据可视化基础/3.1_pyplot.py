# 代码 3-1
import numpy as np
import matplotlib.pyplot as plt
## %matplotlib inline表示在行中显示图片，在命令行运行报错
data = np.arange(0,1.1,0.01)
plt.title('lines') ## 添加标题
plt.xlabel('x')## 添加x轴的名称
plt.ylabel('y')## 添加y轴的名称
plt.xlim((0,1))## 确定x轴范围
plt.ylim((0,1))## 确定y轴范围
plt.xticks([0,0.2,0.4,0.6,0.8,1])## 规定x轴刻度
plt.yticks([0,0.2,0.4,0.6,0.8,1])## 确定y轴刻度
plt.plot(data,data**2)## 添加y=x^2曲线
plt.plot(data,data**4)## 添加y=x^4曲线
plt.legend(['y=x^2','y=x^4'])
plt.savefig('./tmp/y=x^2.png')
#plt.show()

# 代码 3-2
rad = np.arange(0,np.pi*2,0.01)
##第一幅子图
p1 = plt.figure(figsize=(8,6),dpi=80)## 确定画布大小
ax1 = p1.add_subplot(2,1,1)## 创建一个两行1列的子图，并开始绘制第一幅
plt.title('lines')## 添加标题
plt.xlabel('x')## 添加x轴的名称
plt.ylabel('y')## 添加y轴的名称
plt.xlim((0,1))## 确定x轴范围
plt.ylim((0,1))## 确定y轴范围
plt.xticks([0,0.2,0.4,0.6,0.8,1])## 规定x轴刻度
plt.yticks([0,0.2,0.4,0.6,0.8,1])## 确定y轴刻度
plt.plot(rad,rad**2)## 添加y=x^2曲线
plt.plot(rad,rad**4)## 添加y=x^4曲线
plt.legend(['y=x^2','y=x^4'])

##第二幅子图
ax2 = p1.add_subplot(2,1,2)## 创开始绘制第2幅
plt.title('sin/cos') ## 添加标题
plt.xlabel('rad')## 添加x轴的名称
plt.ylabel('value')## 添加y轴的名称
plt.xlim((0,np.pi*2))## 确定x轴范围
plt.ylim((-1,1))## 确定y轴范围
plt.xticks([0,np.pi/2,np.pi,np.pi*1.5,np.pi*2])## 规定x轴刻度
plt.yticks([-1,-0.5,0,0.5,1])## 确定y轴刻度
plt.plot(rad,np.sin(rad))## 添加sin曲线
plt.plot(rad,np.cos(rad))## 添加cos曲线
plt.legend(['sin','cos'])
plt.savefig('./tmp/sincos.png')
plt.show()

# 代码 3-3
## 原图
x = np.linspace(0, 4*np.pi)## 生成x轴数据
y = np.sin(x)## 生成y轴数据
plt.plot(x,y,label="$sin(x)$")## 绘制sin曲线图
plt.title('sin')
plt.savefig('./tmp/默认sin曲线.png')
plt.show()

## 修改rc参数后的图
plt.rcParams['lines.linestyle'] = '-.'#-，-.，--，：四种
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['lines.marker']='D' #线的形状
plt.plot(x,y,label="$sin(x)$")## 绘制三角函数
plt.title('sin')
plt.savefig('./tmp/修改rc参数后sin曲线.png')
plt.show()

# 代码 3-4
## 无法显示中文标题
plt.plot(x,y,label="$sin(x)$")## 绘制三角函数
plt.title('sin曲线')
plt.savefig('./tmp/无法显示中文标题sin曲线.png')
plt.show()

##设置rc参数显示中文标题
## 设置字体为SimHei显示中文
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False ## 设置正常显示符号
plt.plot(x,y,label="$sin(x)$")## 绘制三角函数
plt.title('sin曲线')
plt.savefig('./tmp/显示中文标题sin曲线.png')
plt.show()

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

# 代码 3-5
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
data = np.load('D:/软件（学习）/Python/数据分析与挖掘/chapter3/data/国民经济核算季度数据.npz')
data = np.load('./data/国民经济核算季度数据.npz')

name = data['columns'] ## 提取其中的columns数组，视为数据的标签
values = data['values']## 提取其中的values数组，数据的存在位置\
print(data['columns'])
print(data['values'])

plt.figure(figsize=(8,7))## 设置画布
plt.scatter(values[:,0],values[:,2], marker='o')## 绘制散点图
plt.xlabel('年份')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(0,70,4),values[range(0,70,4),1],rotation=45)
plt.title('2000-2017年季度生产总值散点图')## 添加图表标题
plt.savefig('./tmp/2000-2017年季度生产总值散点图.png')
plt.show()


# 代码 3-10
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
data = np.load('./data/国民经济核算季度数据.npz')
name = data['columns']## 提取其中的columns数组，视为数据的标签
values = data['values']## 提取其中的values数组，数据的存在位置
print(name)
print(values)
p = plt.figure(figsize=(12,12)) ##设置画布

## 子图1
ax1 = p.add_subplot(2,1,1)
plt.scatter(values[:,0],values[:,3], marker='o',c='r')## 绘制散点
plt.scatter(values[:,0],values[:,4], marker='D',c='b')## 绘制散点
plt.scatter(values[:,0],values[:,5], marker='v',c='y')## 绘制散点
plt.ylabel('生产总值（亿元）')## 添加纵轴标签
plt.title('2000-2017年各产业季度生产总值散点图')## 添加图表标题
plt.legend(['第一产业','第二产业','第三产业'])## 添加图例

## 子图2
ax2 = p.add_subplot(2,1,2)
plt.scatter(values[:,0],values[:,6], marker='o',c='r')## 绘制散点
plt.scatter(values[:,0],values[:,7], marker='D',c='b')## 绘制散点
plt.scatter(values[:,0],values[:,8], marker='v',c='y')## 绘制散点
plt.scatter(values[:,0],values[:,9], marker='8',c='g')## 绘制散点
plt.scatter(values[:,0],values[:,10], marker='p',c='c')## 绘制散点
plt.scatter(values[:,0],values[:,11], marker='+',c='m')## 绘制散点
plt.scatter(values[:,0],values[:,12], marker='s',c='k')## 绘制散点
## 绘制散点
plt.scatter(values[:,0],values[:,13], marker='*',c='purple')
## 绘制散点
plt.scatter(values[:,0],values[:,14], marker='d',c='brown')
plt.legend(['农业','工业','建筑','批发','交通''餐饮','金融','房地产','其他'])
plt.xlabel('年份')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加纵轴标签
plt.xticks(range(0,70,4),values[range(0,70,4),1],rotation=45)
plt.savefig('./tmp/2000-2017年季度各行业生产总值散点子图.png')
plt.show()

# 代码 3-11
p1 = plt.figure(figsize=(8,7))## 设置画布
## 子图1
ax3 = p1.add_subplot(2,1,1)
plt.plot(values[:,0],values[:,3],'b-',
        values[:,0],values[:,4],'r-.',
        values[:,0],values[:,5],'g--')## 绘制折线图
plt.ylabel('生产总值（亿元）')## 添加纵轴标签
plt.title('2000-2017年各产业季度生产总值折线图')## 添加图表标题
plt.legend(['第一产业','第二产业','第三产业'])## 添加图例
## 子图2
ax4 = p1.add_subplot(2,1,2)
plt.plot(values[:,0],values[:,6], 'r-',## 绘制折线图
        values[:,0],values[:,7], 'b-.',## 绘制折线图
        values[:,0],values[:,8],'y--',## 绘制折线图
        values[:,0],values[:,9], 'g:',## 绘制折线图
        values[:,0],values[:,10], 'c-',## 绘制折线图
        values[:,0],values[:,11], 'm-.',## 绘制折线图
        values[:,0],values[:,12], 'k--',## 绘制折线图
        values[:,0],values[:,13], 'r:',## 绘制折线图
        values[:,0],values[:,14], 'b-')## 绘制折线图
plt.legend(['农业','工业','建筑','批发','交通','餐饮','金融','房地产','其他'])
plt.xlabel('年份')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加纵轴标签
plt.xticks(range(0,70,4),values[range(0,70,4),1],rotation=45)
plt.savefig('./tmp/2000-2017年季度各行业生产总值折线子图.png')
plt.show()


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

# 代码 3-15
import numpy as np
import matplotlib.pyplot as plt
data = np.load('./data/国民经济核算季度数据.npz')
name = data['columns'] ## 提取其中的columns数组，视为数据的标签
values = data['values']## 提取其中的values数组，数据的存在位置
print(data)
print(values)
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
label1 = ['第一产业','第二产业','第三产业']## 刻度标签1
label2 = ['农业','工业','建筑','批发','交通',
        '餐饮','金融','房地产','其他']## 刻度标签2
p = plt.figure(figsize=(12,12))

## 子图1
ax1 = p.add_subplot(2,2,1)
plt.bar(range(3),values[0,3:6],width = 0.5)## 绘制散点图
plt.xlabel('产业')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(3),label1)
plt.title('2000年第一季度国民生产总值产业构成分布直方图')

## 子图2
ax2 = p.add_subplot(2,2,2)
plt.bar(range(3),values[-1,3:6],width = 0.5)## 绘制散点图
plt.xlabel('产业')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(3),label1)
plt.title('2017年第一季度国民生产总值产业构成分布直方图')

## 子图3
ax3 = p.add_subplot(2,2,3)
plt.bar(range(9),values[0,6:],width = 0.5)## 绘制散点图
plt.xlabel('行业')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(9),label2)
plt.title('2000年第一季度国民生产总值行业构成分布直方图')## 添加图表标题

## 子图4
ax4 = p.add_subplot(2,2,4)
plt.bar(range(9),values[-1,6:],width = 0.5)## 绘制散点图
plt.xlabel('行业')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称
plt.xticks(range(9),label2)
plt.title('2017年第一季度国民生产总值行业构成分布直方图')## 添加图表标题

## 保存并显示图形
plt.savefig('./tmp/国民生产总值构成分布直方图.png')
plt.show()

# 代码 3-16
label1 = ['第一产业','第二产业','第三产业']## 标签1
label2 = ['农业','工业','建筑','批发','交通',
        '餐饮','金融','房地产','其他']## 标签2
explode1 = [0.01,0.01,0.01]
explode2 = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
p = plt.figure(figsize=(12,12))

## 子图1
ax1 = p.add_subplot(2,2,1)
plt.pie(values[0,3:6],explode=explode1,labels=label1,
        autopct='%1.1f%%')## 绘制散点图
plt.title('2000年第一季度国民生产总值产业构成分布饼图')

## 子图2
ax2 = p.add_subplot(2,2,2)
plt.pie(values[-1,3:6],explode=explode1,labels=label1,
        autopct='%1.1f%%')## 绘制散点图
plt.title('2017年第一季度国民生产总值产业构成分布饼图')

## 子图3
ax3 = p.add_subplot(2,2,3)
plt.pie(values[0,6:],explode=explode2,labels=label2,
        autopct='%1.1f%%')## 绘制散点图
plt.title('2000年第一季度国民生产总值行业构成分布饼图')## 添加图表标题

## 子图4
ax4 = p.add_subplot(2,2,4)
plt.pie(values[-1,6:],explode=explode2,labels=label2,
        autopct='%1.1f%%')## 绘制散点图
plt.title('2017年第一季度国民生产总值行业构成分布饼图')## 添加图表标题

## 保存并显示图形
plt.savefig('./tmp/国民生产总值构成分布饼图.png')
plt.show()


# 代码 3-17
label1 = ['第一产业','第二产业','第三产业']## 标签1
label2 = ['农业','工业','建筑','批发','交通',
        '餐饮','金融','房地产','其他']## 标签2
gdp1 = (list(values[:,3]),list(values[:,4]),list(values[:,5]))
gdp2 = ([list(values[:,i]) for i in range(6,15)])
p = plt.figure(figsize=(8,8))

## 子图1
ax1 = p.add_subplot(2,1,1)
## 绘制散点图
plt.boxplot(gdp1,notch=True,labels = label1, meanline=True)
plt.title('2000-2017各产业国民生产总值箱线图')
plt.ylabel('生产总值（亿元）')## 添加y轴名称

## 子图2
ax2 = p.add_subplot(2,1,2)
## 绘制散点图
plt.boxplot(gdp2,notch=True,labels = label2, meanline=True)
plt.title('2000-2017各行业国民生产总值箱线图')
plt.xlabel('行业')## 添加横轴标签
plt.ylabel('生产总值（亿元）')## 添加y轴名称

## 保存并显示图形
plt.savefig('./tmp/国民生产总值分散情况箱线图.png')
plt.show()