import json
import random
import requests
class ProxyMiddleware(object):
    def __init__(self):
        ret = requests.get("http://proxy.httpdaili.com/apinew.asp?text=true&noinfo=true&sl=10&ddbh=gs921302")
        ip_list = ret.text.split("\r\n")
        ip_list.pop(-1)
        ip_list.append("124.47.7.38:80")
        ip_list.append("183.129.244.17:31773")
        ip_list.append("115.213.254.158:9000")
        ip_list.append("111.202.37.195:47818")
        ip_list.append("183.129.207.84:55983")
        with open("./yhd/proxy.json",'w') as f:
            ip_list = json.dumps(ip_list)
            f.write(ip_list)

        with open('./yhd/proxy.json', 'r') as f:
            self.proxies = json.load(f)
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))
