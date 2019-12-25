# -*- coding: utf-8 -*-
import json
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import ArticalItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        item = ArticalItem()
        text = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        json_data = json.loads(text)

        item['title'] = json_data['props']['initialState']['note']['data']['public_title']
        item['content'] = json_data['props']['initialState']['note']['data']['free_content']
        item['artical_id'] = json_data['props']['initialState']['note']['data']['id']
        item['origin_url'] = response.url
        pub_time = datetime.utcfromtimestamp(int(json_data['props']['initialState']['note']['data']['first_shared_at']))
        item['pub_time'] = pub_time.strftime("%Y-%m-%d %H:%M:%S")
        item['likes_count'] = json_data['props']['initialState']['note']['data']['likes_count']
        item['views_count'] = json_data['props']['initialState']['note']['data']['views_count']
        item['comments_count'] = json_data['props']['initialState']['note']['data']['comments_count']
        item['slug'] = json_data['props']['initialState']['note']['data']['slug']
        item['words_num'] = json_data['props']['initialState']['note']['data']['wordage']
        item['notebook_id'] = json_data['props']['initialState']['note']['data']['notebook_id']
        item['author_name'] = json_data['props']['initialState']['note']['data']['user']['nickname']
        item['author_id'] = json_data['props']['initialState']['note']['data']['user']['id']
        item['description'] = json_data['props']['initialState']['note']['data']['description']

        item['user_following_count'] = json_data['props']['initialState']['note']['data']['user']['following_count']
        item['user_gender'] = json_data['props']['initialState']['note']['data']['user']['gender']
        item['user_intro'] = json_data['props']['initialState']['note']['data']['user']['intro'].replace('\n', '')
        item['user_likes_count'] = json_data['props']['initialState']['note']['data']['user']['likes_count']
        item['user_slug'] = json_data['props']['initialState']['note']['data']['user']['slug']
        item['user_avatar'] = json_data['props']['initialState']['note']['data']['user']['avatar']
        item['user_words_num'] = json_data['props']['initialState']['note']['data']['user']['wordage']
        return item
