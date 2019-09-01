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
ax1=p.add_subplot(2,2,1)
plt.bar(range(1,41,2),data[:-2,2],width=0.5)
plt.bar(range(2,41,2),data[:-2,3],width=0.5)
plt.xlabel('年份') #添加横轴标签
plt.ylabel('人口（万）')## 添加y轴名称
plt.title('1996——2015人口关系数据特征男女人口比例直方图')## 添加图表标题
plt.xticks(range(2,41,2),data[range(0,20),0],rotation=45)
plt.legend(feature_names[2:4])

ax2=p.add_subplot(2,2,2)
plt.bar(range(1,41,2),data[:-2,4],width=0.5)
plt.bar(range(2,41,2),data[:-2,5],width=0.5)
plt.xlabel('年份') #添加横轴标签
plt.ylabel('人口（万）')## 添加y轴名称
plt.title('1996——2015人口关系数据特征城乡人口数目直方图')## 添加图表标题
plt.xticks(range(2,41,2),data[range(0,20),0],rotation=45)
plt.legend(feature_names[4:6])

ax3=p.add_subplot(2,2,3)
#explode=[0.01,0.01,0.01,0.01]
label=data[0:-2,0]
plt.pie(data[:-2,2]/data[:-2,3],labels=label,autopct='%1.1f%%')
plt.title('1996——2015人口关系数据特征男女人口比例饼图')## 添加图表标题

ax4=p.add_subplot(2,2,4)
#explode=[0.01,0.01,0.01,0.01]
label=data[0:-2,0]
plt.pie(data[:-2,4]/data[:-2,5],labels=label,autopct='%1.1f%%')
plt.title('1996——2015人口关系数据特征城乡人口比例饼图')## 添加图表标题
plt.savefig('./tmp/1996——2015人口关系数据特征散点图与折线图与饼图.png')
plt.show()