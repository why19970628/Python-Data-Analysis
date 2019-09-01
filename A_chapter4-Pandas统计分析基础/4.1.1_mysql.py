# 代码 4-1
from sqlalchemy import create_engine
## 创建一个mysql连接器，用户名为root，密码为1234
## 地址为127.0.0.1，数据库名称为testdb，编码为utf-8
engine = create_engine('mysql+pymysql://root:root@localhost/testdb?charset=utf8')
print(engine)

# 代码 4-2
import pandas as pd
## 使用read_sql_query查看tesdb中的数据表数目
formlist = pd.read_sql_query('show tables', con = engine)
print('testdb数据库数据表清单为:','\n',formlist)

## 使用read_sql_table读取订单详情表
detail1 = pd.read_sql_table('meal_order_detail1',con = engine)
print('使用read_sql_table读取订单详情表的长度为:',len(detail1))

## 使用read_sql读取订单详情表
detail2 = pd.read_sql('select * from meal_order_detail2',con = engine)
print('使用read_sql函数+sql语句读取的订单详情表长度为:',len(detail2))
detail3 = pd.read_sql('meal_order_detail3',con = engine)
print('使用read_sql函数+表格名称读取的订单详情表长度为:',len(detail3))

# 代码 4-3
## 使用to_sql存储orderData
detail1.to_sql('test1',con = engine,index = False,if_exists = 'replace')
## 使用read_sql读取test表
formlist1 = pd.read_sql_query('show tables',con = engine)
print('新增一个表格后testdb数据库数据表清单为：','\n',formlist1)
