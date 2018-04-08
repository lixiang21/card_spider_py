# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from requests import RequestException
import re
import json

headers = {'User-Agent':'Mozilla/5.0 '}

def get_one_page(url):
    try:
        res = requests.get(url,headers = headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_card_url(hash_id):
    url = "https://www.ourocg.cn/card/%s" % hash_id
    html = get_one_page(url)
    soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
    for node in soup.find_all(attrs={"class": "val el-col-xs-18 el-col-sm-12 el-col-md-14 el-col-sm-pull-8 el-col-md-pull-6"}):
        print node.get_text().strip()

    for node in soup.find_all(attrs={"class": "val el-col-xs-6 el-col-sm-4"}):
        print node.get_text().strip()

    for node in soup.find_all(attrs={"class": "val el-col-xs-18 el-col-sm-4"}):
        print node.get_text().strip()

    for node in soup.find_all(attrs={"class": "val el-col-xs-6 el-col-sm-12"}):
        print node.get_text().strip()

    for node in soup.find_all(attrs={"class": "val el-col-24 effect"}):
        print node.get_text().strip()

    for node in soup.find_all(attrs={"class" :"img"}):
        i = node.div["style"].find("(")
        j = node.div["style"].find(")")
        print node.div["style"][i+2:j-1]



if __name__ == '__main__':
    for i in range(1, 2):
        url = 'https://www.ourocg.cn/card/list-5/%d' % i
        html = get_one_page(url)
        soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
        for node in soup.find_all('script'):
            text = node.get_text()
            idx = text.find("window.__STORE__")
            if idx != -1:
                text = text[idx+19:len(text)-2]
                data = json.loads(text)
                for card in  data["cards"]:
                    hash_id = card["hash_id"]
                    parse_card_url(hash_id)
                
                

