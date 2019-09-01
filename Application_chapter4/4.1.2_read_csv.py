import pandas as pd
# 代码 4-4
## 使用read_table读取订单信息表
order = pd.read_table('./data/meal_order_info.csv',sep = ',',encoding = 'gbk')
print('使用read_table读取的订单信息表的长度为：',len(order))

## 使用read_csv读取订单信息表
order1 = pd.read_csv('./data/meal_order_info.csv',encoding = 'gbk')
print('使用read_csv读取的订单信息表的长度为：',len(order1))

# 代码 4-5
## 使用read_table读取菜品订单信息表,sep = ';'
order2 = pd.read_table('./data/meal_order_info.csv',sep = ';',encoding = 'gbk')
print('分隔符为;时订单信息表为：\n',order2)

## 使用read_csv读取菜品订单信息表,header=None
order3 = pd.read_csv('./data/meal_order_info.csv',sep = ',',header = None,encoding = 'gbk')
print('订单信息表为：','\n',order3)

# 代码 4-6
import os
print('订单信息表写入文本文件前目录内文件列表为：\n',os.listdir('./tmp'))
## 将order以csv格式存储
order.to_csv('./tmp/orderInfo.csv',sep = ';',index = False)
print('订单信息表写入文本文件后目录内文件列表为：\n',os.listdir('./tmp'))

# 代码 4-7
user = pd.read_excel('./data/users.xlsx')## 读取user.xlsx文件
print('客户信息表长度为：',len(user))

# 代码 4-8
print('客户信息表写入excel文件前目录内文件列表为：\n',os.listdir('./tmp'))
user.to_excel('./tmp/userInfo.xlsx')
print('客户信息表写入excel文件后目录内文件列表为：\n',os.listdir('./tmp'))




