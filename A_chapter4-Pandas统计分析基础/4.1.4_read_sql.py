# 代码 4-9
## 导入SQLAlchemy库的creat_engine函数
from sqlalchemy import create_engine
import pandas as pd
## 创建一个mysql连接器，用户名为root，密码为1234
## 地址为127.0.0.1，数据库名称为testdb
engine = create_engine('mysql+pymysql://root:root@localhost/testdb?charset=utf8')
## 使用read_sql_table读取订单详情表格
order1 = pd.read_sql_table('meal_order_detail1',con = engine)
print('订单详情表1的长度为:',len(order1))
order2 = pd.read_sql_table('meal_order_detail2',con = engine)
print('订单详情表2的长度为:',len(order2))
order3 = pd.read_sql_table('meal_order_detail3',con = engine)
print('订单详情表3的长度为:',len(order3))

# 代码 4-10
## 使用read_table读取订单信息表
orderInfo = pd.read_table('./data/meal_order_info.csv',sep = ',',encoding = 'gbk')
print('订单信息表的长度为：',len(orderInfo))
# 代码 4-11
## 读取user.xlsx文件
userInfo = pd.read_excel('./data/users.xlsx',  sheetname = 'users1')
print('客户信息表的长度为：',len(userInfo))


