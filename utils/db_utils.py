import pymysql
from pymysql.cursors import DictCursor


# 数据库工具类
class DBUtils:

    def __init__(self,host,port,user,password,database):
        self.conn=pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset="utf8mb4",
            # 返回值为字典
            cursorclass=DictCursor,
            autocommit=True  # 查询操作可以自动提交  如果为False 可以手动进行事务的管理
        )

    def query_one(self,sql,params=None):
        # 查询单条记录
        # with自动管理 确认游标使用完之后自动关闭
        # 相当于：
        # cursor = self.conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     result = cursor.fetchone()
        # finally:
        #     cursor.close()  # 必须手动关闭

        #self,conn,cursor()建立数据库连接
        with self.conn.cursor() as cursor:
            cursor.execute(sql,params)
            # 返回第一条匹配的数据
            return cursor.fetchone()

    # 添加参数防止sql注入
    def query_all(self, sql,params=None):
        # 查询多条记录，返回 list[dict]
        with self.conn.cursor() as cursor:
            cursor.execute(sql,params)
            # 返回多条数据
            return cursor.fetchall()

    def close(self):
        self.conn.close()