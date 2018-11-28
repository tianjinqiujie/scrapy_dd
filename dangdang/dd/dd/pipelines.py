# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import requests


class DdPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipline(object):
    return_list = []

    def process_item(self, item, spider):
        self.return_list.append(dict(item))

        while len(self.return_list) > 10:
            data = {
                "info": "操作完成",
                "code": 200,
                "data": self.return_list
            }
            url = "http://bgpy.wantupai.com/server/api/goods/import"
            data_info = json.dumps(data)
            form_data = {"data": data_info}
            s = requests.post(url, data=form_data)
            self.return_list = []

            print("--------------->", s.text)
