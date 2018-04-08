# -*- coding:utf-8 -*-
import json

import requests
import pymysql
import time
from bs4 import BeautifulSoup
from requests import RequestException

headers = {'User-Agent': 'Mozilla/5.0 '}

# create conn
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='ygoh', charset='utf8')
cursor = conn.cursor()


def get_one_page(url):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None


def parse_card_url(hash_id):
    try:
        data = {}
        url = "https://www.ourocg.cn/card/%s" % hash_id
        html = get_one_page(url)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        soups = soup.find_all(attrs={"class": "val el-col-xs-18 el-col-sm-12 el-col-md-14 el-col-sm-pull-8 el-col-md-pull-6"})
        data["name_cn"], data["name_jp"], data["name_us"], data["category"], data["code"] = [node.get_text().strip() for node in soups]
        data["category"] = "|".join(data["category"].split("\n"))

        soups = soup.find_all(attrs={"class": "val el-col-xs-6 el-col-sm-4"})
        if len(soups) != 0:
            data["race"], data["property"], data["atk"] = [node.get_text().strip() for node in soups]
        else:
            data["race"], data["property"], data["atk"] = [u"", u"", u"0"]

        for node in soup.find_all(attrs={"class": "val el-col-xs-18 el-col-sm-4"}):
            data["level"] = node.get_text().strip()

        for node in soup.find_all(attrs={"class": "val el-col-xs-6 el-col-sm-12"}):
            data["def"] = node.get_text().strip()

        for node in soup.find_all(attrs={"class": "val el-col-24 effect"}):
            data["desc"] = node.get_text().strip()

        for node in soup.find_all(attrs={"class": "img"}):
            i = node.div["style"].find("(")
            j = node.div["style"].find(")")
            data["url"] = node.div["style"][i + 2:j - 1]

        sql = """INSERT INTO cards (name_cn, name_jp, name_us, category, code, race, property, level, atk, def, `desc`, url) VALUES 
                ("%s","%s","%s","%s","%d","%s","%s","%d","%d","%d","%s", "%s")""" % (
            data["name_cn"].encode("utf8"),
            data["name_jp"].encode("utf8"),
            data["name_us"].encode("utf8"),
            data["category"].encode("utf8"),
            int(data["code"]),
            data["race"].encode("utf8"),
            data["property"].encode("utf8"),
            int(data["level"]) if data.has_key("level") else 0,
            int(data["atk"]) if data.has_key("atk") else 0,
            int(data["def"]) if data.has_key("def") else 0,
            data["desc"].encode("utf8"),
            data["url"].encode("utf8"),
        )
        print sql
        cursor.execute(sql)
        conn.commit()
    except Exception, e:
        print e


if __name__ == '__main__':
    try:
        for i in range(1, 893):
            time.sleep(5)
            try:
                print i
                url = 'https://www.ourocg.cn/card/list-5/%d' % i
                html = get_one_page(url)
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                for node in soup.find_all('script'):
                    text = node.get_text()
                    idx = text.find("window.__STORE__")
                    if idx != -1:
                        text = text[idx + 19:len(text) - 2]
                        data = json.loads(text)
                        for card in data["cards"]:
                            hash_id = card["hash_id"]
                            parse_card_url(hash_id)
            except Exception, e:
                print e
        cursor.close()
        conn.close()
    except Exception, e:
        print e
