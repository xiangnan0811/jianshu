# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from jianshu.db.dbhelper import DBHelper


class JianshuPipeline:
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'weibo',
            'password': 'qwe123',
            'database': 'jianshu',
            'charset': 'utf8mb4'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        # self.cursor.execute(self.sql2, (user['user_id'], user['nickname'], user['gender'], user['intro'], user['slug'], user['following_count'], user['avatar'], user['likes_count'], user['words_num']))
        self.cursor.execute(self.sql, (item['title'], item['content'], item['artical_id'], item['origin_url'], item['pub_time'], item['likes_count'], item['views_count'], item['comments_count'], item['slug'], item['words_num'], item['notebook_id'], item['author_name'], item['author_id'], item['description']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = "INSERT INTO artical(id, title, content, artical_id, origin_url, pub_time, likes_count, views_count, comments_count, slug, words_num, notebook_id, author_name, author_id, description) " \
                        "VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            return self._sql
        return self._sql


class JianshuTwistedPipline:
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'weibo',
            'password': 'qwe123',
            'database': 'jianshu',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = "INSERT INTO artical(id, title, content, artical_id, origin_url, pub_time, likes_count, views_count, comments_count, slug, words_num, notebook_id, author_name, author_id, description) " \
                        "VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            return self._sql
        return self._sql

    def process_item(self, artical, spider):
        query = self.dbpool.runInteraction(self.insert_item, artical)
        query.addErrback(self.handle_error, artical, spider)

    def insert_item(self, cursor, item):
        params = (item['title'], item['content'], item['artical_id'], item['origin_url'], item['pub_time'],
                  item['likes_count'], item['views_count'], item['comments_count'], item['slug'],
                  item['words_num'], item['notebook_id'], item['author_name'], item['author_id'],
                  item['description'])
        cursor.execute(self.sql, params)

    def handle_error(self, error, item, spider):
        if error:
            # 打印错误信息
            print('*'*20+'error'+'*'*20)
            print(error)
            print('*'*20+'error'+'*'*20)


class JianshuDBHelperPipline:
    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        self.db.insert_artical(item)
        self.db.insert_user(item)
        return item