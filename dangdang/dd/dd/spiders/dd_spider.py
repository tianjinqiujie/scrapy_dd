# -*- coding: utf-8 -*-
import scrapy
import requests
import time

from dd.items import DDItem
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

headers = {
    "Accept": "text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en;q=0.3,en-US;q=0.2",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "category.dangdang.com",
    "Pragma": "no-cache",
    "Referer": "http://www.dangdang.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/63.0"
}


class DdSpiderSpider(scrapy.Spider):
    name = 'dd_spider'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/?ref=www-0-C/']

    def parse(self, response):
        href = response.css(".classify_books > div > ul > li > a::attr(href)").extract()
        for url in href:
            yield scrapy.Request(url, headers=headers, callback=self.get_next_page)

    def get_next_page(self, response):
        pattern = "http://category\.dangdang\.com/pg.*"
        le = LinkExtractor(allow=pattern)
        try:
            links = le.extract_links(response)[-1]
        except IndexError as e:
            links = le.extract_links(response)
        url_pop = response.url.split("/").pop(-1)
        msg = {"url_pop": url_pop}
        try:
            for i in range(1, int(links.text) + 1):
                url = "http://category.dangdang.com/pg%s-%s" % (i, url_pop)
                yield scrapy.Request(url, meta=msg, callback=self.get_shops_list)
        except ValueError as e:
            yield scrapy.Request(response.url, meta=msg, callback=self.get_shops_list)

        except AttributeError as e:
            pass

    def get_shops_list(self, response):
        msg = response.meta
        url = response.css(".bigimg> li > p > a:nth-child(1)::attr(href)").extract()
        for i in url:
            yield scrapy.Request(i, meta=msg, callback=self.get_shop_info)

    def get_total_score(self, response):
        print(response.text)

    def get_shop_info(self, response):
        msg = response.meta.get("url_pop").lstrip("cp").rstrip(".html")
        price = response.xpath("//div[@class='price_d']/p[@id='dd-price']").extract_first()
        if not price:
            price = response.xpath("//div[@class='cost_box']/p[1]/span[@class='normal_price']/i/text()").extract_first()
        price_soup = BeautifulSoup(price, "html")
        if not price_soup:
            return

        ########################################### 获取所需数据 ###########################################
        # 价格
        goods_price = price_soup.text.strip('\n').strip("\r").strip(" ").lstrip("¥")
        try:
            goods_price = float(goods_price)
        except ValueError as e:
            goods_price = float(goods_price.split("-")[0])

        # 名称
        goods_name = response.xpath("/html/body/div[2]/div[3]/div[2]/div/div[1]/div[1]/h1/@title").extract_first()
        if not goods_name:
            goods_name = str(response.css(".name_info > h1:nth-child(1)").extract_first())
        goods_name_soup = BeautifulSoup(goods_name)
        goods_name = goods_name_soup.text.replace("\r","").strip(" ").replace("\n","").strip(" ").replace(" ","")

        # 商品链接
        goods_detail_url = response.url

        # 图片链接
        goods_image = response.css("#main-img-slider > li > a > img::attr(src)").extract_first()

        # 商品ID
        goods_product_id = int(response.url.split("/")[-1].split(".")[-2])

        # 商品分类名称
        goods_cate_name = response.css("a.green:nth-child(1)::text").extract_first()

        # 评论数/销量
        goods_comment_num = response.css("#comm_num_down::text").extract_first()

        # 商铺名称

        shop_name = response.css(".title_name > span:nth-child(2) > a:nth-child(1)::text").extract_first()
        if not shop_name:
            shop_name = "当当自营"

        # 评分

        url = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId={}&categoryPath={}' \
              '&mainProductId={}&mediumId=0&pageIndex=1&sortType=1&filterType=1&isSystem=1&tagId=0&' \
              'tagFilterCount=0'.format(goods_product_id, msg, goods_product_id)

        time.sleep(0.1)
        # ret = scrapy.Request(url,callback=self.get_total_score)


        s = requests.Session()

        goods_total_score = float(s.get(url).json().get('data').get("list").get('summary').get('goodRate')) / 20


        dd = DDItem()
        info = {
            "goods_price": goods_price,
            "goods_name": goods_name,
            "goods_detail_url": goods_detail_url,
            "goods_image": goods_image,
            "goods_product_id": goods_product_id,
            "goods_cate_name": goods_cate_name,
            "goods_comment_num": goods_comment_num,
            "goods_sale_num": goods_comment_num,
            "shop_name": shop_name,
            "goods_total_score": goods_total_score,
            "platform": 9
        }

        dd["goods_price"] = goods_price
        dd["goods_name"] = goods_name
        dd["goods_detail_url"] = goods_detail_url
        dd["goods_image"] = goods_image
        dd["goods_product_id"] = goods_product_id
        dd["goods_cate_name"] = goods_cate_name
        dd["goods_comment_num"] = goods_comment_num
        dd["goods_sale_num"] = goods_comment_num
        dd["shop_name"] = shop_name
        dd["goods_total_score"] = goods_total_score
        dd["platform"] = 9


        yield dd



        # print("----->", info)
