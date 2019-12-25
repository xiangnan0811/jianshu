import pymysql
from scrapy.utils.project import get_project_settings  # 引入settings配置


class DBHelper:
    def __init__(self):
        self.settings = get_project_settings()  # 获取settings配置数据

        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    # 连接mysql
    def connectmysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8mb4')
        return conn

    # 连接数据库
    def connectdatabase(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8mb4')
        return conn

    # 创建数据库
    def createdatabase(self):
        conn = self.connectmysql()

        sql = "create database if not exists "+self.db
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 创建数据表
    def createtable(self, sql):
        conn = self.connectdatabase()

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 插入数据
    def insert(self, sql, *params):
        conn = self.connectdatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    # 更新数据
    def update(self, sql, *params):
        conn = self.connectdatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    # 删除数据
    def delete(self, sql, *params):
        conn = self.connectdatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


