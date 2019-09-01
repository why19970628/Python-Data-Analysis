# 代码 9-1
import pandas as pd
import numpy as np
data = pd.read_excel('../data/original_data.xls')
print('初始状态的数据形状为：', data.shape)
# 删除热水器编号，有无水流，节能模式
data.drop(labels = ["热水器编号","有无水流","节能模式"],axis = 1,inplace = True)
print('删除冗余特征后的数据形状为：', data.shape)
data.to_csv('../tmp/water_heart.csv',index = False)

# 代码 9-2
threshold = pd.Timedelta('4 min') #阈值为分钟
data['发生时间'] = pd.to_datetime(data['发生时间'], format = '%Y%m%d%H%M%S') # 转换时间格式
data = data[data['水流量'] > 0] #只要流量大于0的记录
#相邻时间向前差分，比较是否大于阈值
sjKs = data['发生时间'].diff() > threshold  #numpy.diff(a, n=1,axis=-1)沿着指定轴计算第N维的离散差值
#参数： a：输入矩阵 n：可选，代表要执行几次差值 axis：默认是最后一个
sjKs.iloc[0] = True # 令第一个时间为第一个用水事件的开始事件
sjJs = sjKs.iloc[1:] # 向后差分的结果
print(sjJs)
# 令最后一个时间作为最后一个用水事件的结束时间
sjJs = pd.concat([sjJs,pd.Series(True)])
#print(sjJs)
# 创建数据框，并定义用水事件序列
sj = pd.DataFrame(np.arange(1,sum(sjKs)+1),columns = ["事件序号"])
sj["事件起始编号"] = data.index[sjKs == 1]+1 # 定义用水事件的起始编号
sj["事件终止编号"] = data.index[sjJs == 1]+1  # 定义用水事件的终止编号
print('当阈值为4分钟的时候事件数目为：',sj.shape[0])
print(sj.head())
sj.to_csv('../tmp/sj.csv',index = False,encoding='utf-8')
