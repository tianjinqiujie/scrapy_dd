# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DDItem(scrapy.Item):
    goods_price = scrapy.Field()
    goods_name = scrapy.Field()
    goods_detail_url = scrapy.Field()
    goods_image = scrapy.Field()
    goods_product_id = scrapy.Field()
    goods_cate_name = scrapy.Field()
    goods_comment_num = scrapy.Field()
    goods_sale_num = scrapy.Field()
    shop_name = scrapy.Field()
    goods_total_score = scrapy.Field()
    platform = scrapy.Field()
