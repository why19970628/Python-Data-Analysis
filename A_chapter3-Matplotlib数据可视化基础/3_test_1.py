import numpy as np
import matplotlib.pyplot as plt
data=np.load('./data/populations.npz')
feature_names=data['feature_names']
#print(data.files)
data=data['data']
print(feature_names)
print(data)
print(len(data))
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

p = plt.figure(figsize=(12,12))
ax1=p.add_subplot(2,1,1)
plt.scatter(range(1,21),data[:-2,1],marker='o',c='r')
plt.scatter(range(1,21),data[:-2,2],marker='D',c='y')
plt.scatter(range(1,21),data[:-2,3],marker='v',c='b')
plt.scatter(range(1,21),data[:-2,4],marker='8',c='g')
plt.scatter(range(1,21),data[:-2,5],marker='p',c='m')
plt.xlabel('年份') #添加横轴标签
plt.ylabel('人口（万）')## 添加y轴名称
label=data[:-3,0]
plt.xticks(range(1,21),data[range(0,20),0],rotation=45)
plt.title('1996——2015人口关系数据特征散点图')## 添加图表标题
plt.legend(feature_names[1:5])

ax2=p.add_subplot(2,1,2)
plt.xlabel('年份') #添加横轴标签
plt.ylabel('人口（万）')## 添加y轴名称
plt.title('1996——2015人口关系数据特征折线图')## 添加图表标题
plt.plot(range(1,21),data[:-2,1],marker='o',c='r')
plt.plot(range(1,21),data[:-2,2],marker='D',c='y')
plt.plot(range(1,21),data[:-2,3],marker='v',c='b')
plt.plot(range(1,21),data[:-2,4],marker='8',c='g')
plt.plot(range(1,21),data[:-2,5],marker='p',c='m')
plt.xticks(range(1,21),data[range(0,20),0],rotation=45)

## 保存并显示图形
plt.savefig('./tmp/1996——2015人口关系数据特征散点图与折线图.png')
plt.show()