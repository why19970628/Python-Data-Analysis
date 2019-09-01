from sqlalchemy import create_engine
import numpy as np
import pandas as pd
## 创建一个mysql连接器，用户名为root，密码为1234
## 地址为127.0.0.1，数据库名称为testdb，编码为utf-8
engine = create_engine('mysql+pymysql://root:root@localhost/testdb?charset=utf8')
detail=pd.read_sql_table('meal_order_detail1',con = engine)
detailPivot= pd.pivot_table(detail[['order_id','counts','amounts']],index= 'order_id')
print('以order_id作为分组键创建的订单透视表为：\n',detailPivot.head())#默认aggfunc=np.mean

# 代码 4-68
detailPivot1 = pd.pivot_table(detail[['order_id','counts','amounts']],index = 'order_id',aggfunc = np.sum)
print('以order_id作为分组键创建的订单销量与售价总和透视表为：\n',detailPivot1.head())

# 代码 4-69
detailPivot2 = pd.pivot_table(detail[['order_id','dishes_name','counts','amounts']],
      index = ['order_id','dishes_name'],aggfunc = np.sum)  ##pivot_table的 index 索引可以有两个
print('以order_id和dishes_name作为分组键创建的订单销量与售价总和透视表为：\n',detailPivot2.head())

# 代码 4-70
detailPivot2 = pd.pivot_table(detail[[
      'order_id','dishes_name','counts','amounts']],
      index = 'order_id',
      columns = 'dishes_name',
      aggfunc = np.sum)
print('以order_id和dishes_name 作为行列分组键 创建的透视表前5行4列为：\n',detailPivot2.iloc[:5,:4])



# 代码 4-71
detailPivot4 = pd.pivot_table(detail[['order_id','dishes_name','counts','amounts']],
      index = 'order_id',
      values = 'counts',
      aggfunc = np.sum)
print('以order_id作为行分组键 counts作为值 创建的透视表前5行为：\n',detailPivot4.head())

# 代码 4-72
detailPivot5 = pd.pivot_table(detail[['order_id','dishes_name','counts','amounts']],
      index = 'order_id',
      columns = 'dishes_name',
      aggfunc = np.sum,
      fill_value = 0)   ###缺失值进行补充 fill_value = 0
print('空值填0后以order_id和dishes_name为行列分组键创建透视表前5行4列为：\n',detailPivot5.iloc[:5,:4])

# 代码 4-73
detailPivot6 = pd.pivot_table(detail[['order_id','dishes_name','counts','amounts']],
      index = 'order_id',columns = 'dishes_name',
      aggfunc = np.sum,fill_value = 0,
      margins = True)
print('添加margins后以order_id和dishes_name为分组键的透视表前5行后4列为：\n',detailPivot6.iloc[:5,-4:])

