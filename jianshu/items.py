# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()                          # 文章名称
    content = scrapy.Field()                        # 文章内容
    artical_id = scrapy.Field()                     # 文章id
    origin_url = scrapy.Field()                     # 文章url
    pub_time = scrapy.Field()                       # 文章发布时间
    likes_count = scrapy.Field()                    # 文章收获点赞数
    views_count = scrapy.Field()                    # 文章阅读量
    comments_count = scrapy.Field()                 # 文章评论数
    slug = scrapy.Field()                           # 文章slug
    words_num = scrapy.Field()                      # 文章字数
    notebook_id = scrapy.Field()                    # 文章notebook_id（目前还不知道是什么量）
    author_name = scrapy.Field()                    # 文章作者昵称
    author_id = scrapy.Field()                      # 文章作者id
    description = scrapy.Field()                    # 文章简介

    user_following_count = scrapy.Field()           # 用户粉丝数
    user_gender = scrapy.Field()                    # 用户性别
    user_slug = scrapy.Field()                      # 用户id
    user_intro = scrapy.Field()                     # 用户简介
    user_likes_count = scrapy.Field()               # 用户收获喜欢数
    user_words_num = scrapy.Field()                 # 用户发文总字数
    user_avatar = scrapy.Field()                    # 用户头像
