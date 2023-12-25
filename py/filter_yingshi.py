##coding=utf-8
#!/usr/bin/python
from base.spider import Spider
from lxml import html,etree
import requests
import json
import re
from pprint import pprint 
from bs4 import BeautifulSoup
from urllib.parse import unquote

def job(typeId):
    items = []
    url = f"https://www.yingshi.tv/vod/show/by/hits_day/id/{typeId}/order/desc.html"  
    doc = BeautifulSoup(requests.get(url).text, 'html.parser')
    items.append(filter(doc.select("div.ys_filter_list_show_types")[0].select("div.ys_filter.flex")[1].select("div > div"), "by", "排序", 4))
    items.append(filter(doc.select("div#ys_filter_by_class")[0].select("div > div"), "class", "類型", 6))
    items.append(filter(doc.select("div#ys_filter_by_country")[0].select("div > div"), "area", "地區", 4))
    items.append(filter(doc.select("div#ys_filter_by_lang")[0].select("div > div"), "lang", "語言", 8))
    items.append(filter(doc.select("div#ys_filter_by_year")[0].select("div > div"), "year", "時間", 10))
    return items

def filter(elements, key, name, index):
    values = []
    for e in elements:
        n = e.select_one("p").text
        all = "全部" in n
        v = "" if all else unquote(e.select_one("a").get("href").split("/")[index].replace(".html", ""))
        values.append({"n": n, "v": v})
    return {"key": key, "name": name, "value": values}


list = {"電視劇": "1","電影": "2","綜藝": "3","動漫": "4","記錄片": "5" }
G = {}
for key in list:   
    n = list[key]
    G[n] = job(n)

G = json.dumps(G, ensure_ascii=False, indent=2)
with open('yingshi.json','w',encoding='utf8') as file:
    file.write(G)           

    
    

