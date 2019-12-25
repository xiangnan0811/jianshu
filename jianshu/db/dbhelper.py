import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置


class DBHelper:
    """这个类也是读取settings中的配置，自行修改代码进行操作"""

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8mb4',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    # 插入文章数据
    def insert_artical(self, item):
        # 这里定义要插入的字段
        sql = "INSERT INTO artical(id, title, content, artical_id, origin_url, pub_time, likes_count, views_count, comments_count, slug, words_num, notebook_id, author_name, author_id, description) " \
              "VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert_artical, sql, item)
        # 调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    # 插入用户数据
    def insert_user(self, item):
        # 这里定义要插入的字段
        sql = "INSERT INTO user(id, user_id, nickname, gender, intro, slug, following_count, avatar, likes_count, words_num) " \
              "VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert_user, sql, item)
        # 调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    # 写入数据库中
    def _conditional_insert_artical(self, canshu, sql, item):
        # 取出要存入的数据，这里item就是爬虫代码爬下来存入items内的数据
        params = (item['title'], item['content'], item['artical_id'], item['origin_url'], item['pub_time'],
                  item['likes_count'], item['views_count'], item['comments_count'], item['slug'],
                  item['words_num'], item['notebook_id'], item['author_name'], item['author_id'],
                  item['description'])
        canshu.execute(sql, params)

    # 写入数据库中
    def _conditional_insert_user(self, canshu, sql, item):
        # 取出要存入的数据，这里item就是爬虫代码爬下来存入items内的数据
        params = (item['author_id'], item['author_name'], item['user_gender'], item['user_intro'], item['user_slug'],
                  item['user_following_count'], item['user_avatar'], item['user_likes_count'], item['user_words_num'])
        canshu.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)
        print('--------------database operation exception!!-----------------')
