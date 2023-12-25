##coding=utf-8
#!/usr/bin/python
from base.spider import Spider
from lxml import html,etree
import requests
import json
import re
from pprint import pprint 
#url = "https://www.yingshi.tv/vod/show/by/time/id/1.html"

'''
rsp = Spider.fetch(None, url)
root = Spider.html(None, Spider.cleanText(None, rsp.text))
aList = root.xpath('/html/body/div/div/section/div/div/li/a')                                                                                                             
videos = []
for a in aList:
    link = a.xpath("./@href")[0]
    if 'vod/play' in link:
        vid = link.split('/')[4]        
        name = (a.xpath('./h2[@class="ys_show_title"]/text()') or [None])[0]
        pic = (a.xpath('./div/img/@src') or [None])[0]
        mark = (a.xpath('.//span[@class="ys_show_episode_text"]/text()') or [None])[0]        
        if name:
            videos.append({"vod_id": vid, "vod_name": name,"vod_pic": pic,"vod_remarks": mark})            
    result = {'list': videos}


print(videos)


import requests
from lxml import html
import json

site_url = "https://www.yingshi.tv"
ids = ["197893"]  # Replace with the actual ID value

url = f"{site_url}/vod/play/id/{ids[0]}/sid/1/nid/1.html"
response = requests.get(url)

tree = html.fromstring(response.text)
json_data = tree.xpath('//script[contains(text(), "let data = ") and contains(text(), "let obj = ")]/text()')[0]
json_data = json_data.split('let data = ')[1].split('let obj = ')[0].strip()[:-1].replace("&amp;", " ")

vod = json.loads(json_data)
result_string = str(vod)

print(result_string)
'''


import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
def call(typeId):
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


gg =''

cateManual = {
        "電視劇": "1",
        "電影": "2",
        "綜藝": "3",
        "動漫": "4",
        "記錄片": "5"
    }

#for k in cateManual:
id = '3'
d = call(id)    
print('{' + id + ':'+ str(d) + '}')
    
    

