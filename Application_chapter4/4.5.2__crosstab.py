from sqlalchemy import create_engine
import numpy as np
import pandas as pd
## 创建一个mysql连接器，用户名为root，密码为1234
## 地址为127.0.0.1，数据库名称为testdb，编码为utf-8
engine = create_engine('mysql+pymysql://root:root@localhost/testdb?charset=utf8')
detail=pd.read_sql_table('meal_order_detail1',con = engine)

# 代码 4-74
detailCross = pd.crosstab(
      index=detail['order_id'],
      columns=detail['dishes_name'],
      values = detail['counts'],
      aggfunc = np.sum)
print('以order_id和dishes_name为分组键counts为值的透视表前5行5列为：\n',detailCross.iloc[:5,:5])


detail=pd.read_sql_table('meal_order_detail1',con=engine)
detail['place_order_time']=pd.to_datetime(detail['place_order_time'])
detail['date']=[i.date() for i in detail['place_order_time']]
Pivot_Detail=pd.pivot_table(detail[['date','dishes_name','counts','amounts']],
        index='date',aggfunc=np.sum,fill_value=0)
print('订单详情表单日菜品成交总额与总数透视表前5行5列为：\n',Pivot_Detail.head())

CrossDetail = pd.crosstab(
      index=detail['date'],columns=detail['dishes_name'],
      values = detail['amounts'],
      aggfunc = np.sum,margins = True)
print('订单详情表单日单个菜品成交总额交叉表后5行5列为：\n',CrossDetail.iloc[-5:,-5:])




