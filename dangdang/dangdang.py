#!/usr/bin/env python
# -*-coding:UTF-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import random
import threading
import time

def wrapprt(func):
    def inner(*args,**kwargs):
        starttime = time.time()
        ret = func(*args,**kwargs)
        endtime = time.time() - starttime
        print(endtime)
        return ret
    return inner


class DangDang(object):
    return_list = []

    @wrapprt
    def search(self, key, num=1, *args, **kwargs):
        for i in range(1, num + 2):
            goods_list = self.get_goods_list(key, i)
            for goods_info_url in goods_list:
                t = threading.Thread(target=self.get_goods_info, args=(goods_info_url,))
                t.start()
        return_msg = {
            "info": "操作完成",
            "code": 200,
            "data": self.return_list
        }
        return return_msg

    def get_goods_list(self, key, page):
        '''
        获取商品列表页面
        :return:
        '''

        url = "http://search.dangdang.com/?key=%s&act=input&page_index=%s" % (key, page)
        URLList = []
        response = requests.get(url).text
        soup = BeautifulSoup(response, from_encoding='utf-8')
        for url in soup.find_all("a"):
            response_url = str(url.get("href")).rstrip("?point=comment_point")
            try:
                if response_url.startswith("http://product"):
                    if response_url not in URLList:
                        URLList.append(response_url)
            except AttributeError as e:
                pass
        return URLList

    def get_goods_info(self, url):
        '''
        获取商品详细信息
        :return:
        '''
        response = requests.get(url)
        response_text = response.text
        soup = BeautifulSoup(response_text, from_encoding='utf-8')
        # 标题
        try:
            title = soup.find("h1").get_text().replace("\r", "").replace(" ", "").replace("\n", "")
        except AttributeError as e:
            title = "---"

        # 价格
        price = soup.find("p", id="dd-price").get_text().lstrip("¥")
        try:
            price = float(price)
        except ValueError as e:
            price = float(price.split("-")[0])
        # 图片
        image_url = re.search("src=\".*?\"", str(soup.find("img", id="largePic"))).group().lstrip("src=").strip("\"")

        # ID
        shops_id = int(response.url.split("/")[-1].split(".")[-2])

        # 商品分类名称
        goods_cate_name = soup.find("a", class_="green").get_text()

        # 评论数/销量
        goods_comment_num = soup.find("a", id="comm_num_down").get_text()

        # 商铺名称
        try:
            shop_name = soup.find("a", attrs={"dd_name": "店铺名称"}).get_text()
        except AttributeError as e:
            shop_name = None
        if not shops_id:
            shop_name = "当当自营"

        # 评分
        goods_total_score = random.choice([4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0])
        if goods_comment_num == "0":
            goods_total_score = 0

        info = {
            "goods_price": price,
            "goods_name": title,
            "goods_detail_url": response.url,
            "goods_image": image_url,
            "goods_product_id": shops_id,
            "goods_cate_name": goods_cate_name,
            "goods_comment_num": goods_comment_num,
            "goods_sale_num": goods_comment_num,
            "shop_name": shop_name,
            "goods_total_score": goods_total_score,
            "platform": 9
        }

        self.return_list.append(info)


if __name__ == '__main__':
    dd = DangDang()
    ret = dd.search("手机")
    print(ret)
