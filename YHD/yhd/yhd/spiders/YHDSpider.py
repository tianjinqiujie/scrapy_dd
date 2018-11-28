# -*- coding: utf-8 -*-
import scrapy
import re
import requests

from yhd.items import YHDIten
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Host": "search.yhd.com",
    "Upgrade-Insecure-Requests": "1",
    "Proxy-Connection": "keep-alive",
    "Cookie": "provinceId=1; cityId=2816; yhd_location=1_2816_6667_0; cart_cookie_uuid=faf88d75-f451-4229-84a0-cbfbf5024854; cart_num=0; shshshfp=6805343cfb76e78e3c0c28b60d0880d7; shshshfpa=b8692046-588c-970b-f8d8-82a0a221aecd-1541586858; shshshfpb=0f31dfc8ce6f6e7e72736621831104614ad12336d1c0fa0fd5be2bfab8; yhd_lastVisit=Wed%20Nov%2007%202018%2019%3A15%3A27%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); guid=JTQG8TH1VSGRS4JWPV9ZR7ETFX63KWUJW32C; unpl=V2_ZzNtbUoCE0EnXEABex4IBGILR19LXhYVdAFCASkbCwA0ABVaclRCFXwURlRnGFoUZwYZXkBcRxRFCEdkex5fDGQzEVRFU0QSdAh2ZHgZbAVmMxJZR1dBFHwORlF7EFwHZAMWWEpfSxxFOEFkS83Jrr%2BIhQ8DFZql0N7s%2BkseWQJhChtYRmdCJXQ4DTp6VFwBYgMQXEtRQxB1AUZWeBlYAG8LGlRyVnMW; JSESSIONID=F4FB9ECEB5534B5EB1E6EA8A759E1F30.s1",
    "Referer": "http://seo.yhd.com/sitelink/sitemap.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}
headers_info = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Host": "item.yhd.com",
    "Upgrade-Insecure-Requests": "1",
    "Proxy-Connection": "keep-alive",
    "Cookie": "provinceId=1; cityId=2816; yhd_location=1_2816_6667_0; cart_cookie_uuid=faf88d75-f451-4229-84a0-cbfbf5024854; cart_num=0; shshshfp=6805343cfb76e78e3c0c28b60d0880d7; shshshfpa=b8692046-588c-970b-f8d8-82a0a221aecd-1541586858; shshshfpb=0f31dfc8ce6f6e7e72736621831104614ad12336d1c0fa0fd5be2bfab8; yhd_lastVisit=Wed%20Nov%2007%202018%2019%3A15%3A27%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); guid=JTQG8TH1VSGRS4JWPV9ZR7ETFX63KWUJW32C; unpl=V2_ZzNtbUoCE0EnXEABex4IBGILR19LXhYVdAFCASkbCwA0ABVaclRCFXwURlRnGFoUZwYZXkBcRxRFCEdkex5fDGQzEVRFU0QSdAh2ZHgZbAVmMxJZR1dBFHwORlF7EFwHZAMWWEpfSxxFOEFkS83Jrr%2BIhQ8DFZql0N7s%2BkseWQJhChtYRmdCJXQ4DTp6VFwBYgMQXEtRQxB1AUZWeBlYAG8LGlRyVnMW; JSESSIONID=F4FB9ECEB5534B5EB1E6EA8A759E1F30.s1",
    "Referer": "http://seo.yhd.com/sitelink/sitemap.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}
headers_price = {
    "Accept": "text/javascript, application/j…ion/x-ecmascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en;q=0.3,en-US;q=0.2",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "provinceId=1; cityId=2816; yhd_location=1_2816_6667_0; cart_cookie_uuid=faf88d75-f451-4229-84a0-cbfbf5024854; cart_num=0; shshshfp=6805343cfb76e78e3c0c28b60d0880d7; shshshfpa=b8692046-588c-970b-f8d8-82a0a221aecd-1541586858; shshshfpb=0f31dfc8ce6f6e7e72736621831104614ad12336d1c0fa0fd5be2bfab8; yhd_lastVisit=Wed%20Nov%2007%202018%2019%3A15%3A27%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); guid=JTQG8TH1VSGRS4JWPV9ZR7ETFX63KWUJW32C; unpl=V2_ZzNtbUoCE0EnXEABex4IBGILR19LXhYVdAFCASkbCwA0ABVaclRCFXwURlRnGFoUZwYZXkBcRxRFCEdkex5fDGQzEVRFU0QSdAh2ZHgZbAVmMxJZR1dBFHwORlF7EFwHZAMWWEpfSxxFOEFkS83Jrr%2BIhQ8DFZql0N7s%2BkseWQJhChtYRmdCJXQ4DTp6VFwBYgMQXEtRQxB1AUZWeBlYAG8LGlRyVnMW; JSESSIONID=A98337EEA52C3F5609B8CCE6037AECD6.s1; shshshsID=b4e6e81bfe799ec9720755ad99e43d95_4_1541731184723",
    "Host": "item.yhd.com",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


class YhdspiderSpider(scrapy.Spider):
    name = 'YHDSpider'
    allowed_domains = ['yhd.com']
    start_urls = ['http://www.yhd.com/']

    def parse(self, response):
        ret = response.xpath('//*[@id="bottomHelpLinkId"]/dl[1]/dd[5]/a/@href').extract_first()
        url = "http:%s" % ret
        yield scrapy.Request(url, callback=self.get_goods_mape)

    def get_goods_mape(self, response):
        ret = response.css("div.map-type > div > div > div > div > div > a::attr(href)").extract()
        for url in ret:
            yield scrapy.Request(url, headers=headers, callback=self.get_next_page)

    def get_next_page(self, response):
        pattern = "http://search.yhd.com/.*"
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        for i in links:
            yield scrapy.Request(i.url, headers=headers, callback=self.get_goods_list)

    def get_goods_list(self, response):
        goods_url = response.css(".proName > a::attr(href)").extract()
        price_list = response.css(".proPrice > em::text").extract()

        price = []
        for i in price_list:
            i = i.replace("\n", '')
            if i:
                price.append(i)
        # print(response.url,price)
        for i in range(len(goods_url)):
            url = "http:%s" % goods_url[i]
            yield scrapy.Request(url, headers=headers_info, meta={"price": price[i]}, callback=self.get_goods_info)

    def get_goods_info(self, response):
        # print(response.text)
        # 第三方ID
        ID = response.url.split("/")[-1].split(".")[0]
        # 商品名称
        title = response.css("#productMainName::text").extract_first()
        if not title:
            return
        headers_price["Referer"] = str(response.url)

        # 图片链接
        image_url = "http://img20.360buyimg.com/n7/s230x230_%s" % response.css(
            "#J_prodImg::attr(original_src)").extract_first()
        # 商家名称
        goods_cate_name = response.css(".crumb > a:nth-child(1) > em:nth-child(1)::text").extract_first()
        platform = 10
        # 商品名称
        shop_name = response.css(".crumb > a > em:nth-child(1)::text").extract()[-1]

        comment_headers = eval(str(headers_price).encode("UTF-8").decode("ISO-8859-1"))
        url = "http://item.yhd.com/squ/comment/getCommentDetail.do?productId=%s" % ID
        s = requests.Session()
        ret = s.get(url, headers=comment_headers, allow_redirects=False).text
        comment_dict = eval(ret).get("value").strip(" ").replace("\n", "").replace("\t", "").replace(" ", "")

        # 评价人数/销量
        comment = re.search('peCount="(?P<comment>.*?)"', comment_dict).group().split("\"")[1]
        #好评
        goods_total_sccore = int(re.search('<spanclass="pct">(\d+)</span>',comment_dict).group().split(">")[1].split("<")[0])//20
        price = response.meta.get("price")
        # print(goods_total_sccore)

        # print(response.url,ID, title, price,image_url,goods_cate_name,shop_name,platform,comment)

        YhdItem = YHDIten()
        YhdItem["platform"] = platform
        YhdItem["goods_name"] = title
        YhdItem["goods_cate_name"] = goods_cate_name
        YhdItem["goods_image"] = image_url
        YhdItem["goods_detail_url"] = response.url
        YhdItem["goods_product_id"] = ID
        YhdItem["goods_price"] = price
        YhdItem["goods_sale_num"] = comment
        YhdItem["goods_total_score"] = goods_total_sccore
        YhdItem["goods_comment_num"] = comment
        YhdItem["shop_name"] = shop_name


        yield YhdItem