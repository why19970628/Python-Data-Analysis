import numpy as np
import matplotlib.pyplot as plt
data=np.load('./data/iris.npz')
print(data.files)
values=data['data'][:,:-1]
name=data['features_name']
print(name)
print(values)
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
p = plt.figure(figsize=(16,16)) ##设置画布
plt.title('iris散点图矩阵')
for i in range(4):
    for j in range(4):
        p.add_subplot(4,4,(i*4)+(j+1))
        plt.scatter(values[:,i],values[:,j])## 绘制散点图
        plt.xlabel(name[i])
        plt.ylabel(name[j])
plt.savefig('./tmp/鸢尾花特征散点图.png')
plt.show()
#箱线图
import numpy as np
import matplotlib.pyplot as plt
data = np.random.normal(size =100 , loc = 0 , scale = 1)
plt.boxplot(data , sym='o' , whis=0.05)
print(data)
plt.show()