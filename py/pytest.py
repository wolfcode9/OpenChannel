from base.spider import Spider
from lxml import html
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

import requests
from bs4 import BeautifulSoup
from typing import List

class Job(List[dict]):

    def __init__(self, typeId):
        self.typeId = typeId

    def __call__(self) -> List[dict]:
        items = []
        url = f"https://www.yingshi.tv/vod/show/by/hits_day/id/{self.typeId}/order/desc.html"
        response = requests.get(url)
        doc = BeautifulSoup(response.text, 'html.parser')
        items.append(self.filter(doc.select("div.ys_filter_list_show_types")[0].select("div.ys_filter.flex")[1].select("div > div"), "by", "排序", 4))
        items.append(self.filter(doc.select("div#ys_filter_by_class")[0].select("div > div"), "class", "類型", 6))
        items.append(self.filter(doc.select("div#ys_filter_by_country")[0].select("div > div"), "area", "地區", 4))
        items.append(self.filter(doc.select("div#ys_filter_by_lang")[0].select("div > div"), "lang", "語言", 8))
        items.append(self.filter(doc.select("div#ys_filter_by_year")[0].select("div > div"), "year", "時間", 10))
        return items

    def filter(self, elements, key, name, index):
        values = []
        for e in elements:
            paragraph = e.select_one("p")
            if paragraph:
                n = paragraph.text
                all_values = "全部" in n
                href = e.select_one("a").get("href") if not all_values else ""
                v = href.split("/")[index].replace(".html", "") if href else ""
                values.append({"n": n, "v": v})
        return {"key": key, "name": name, "values": values}


# Example usage:
job = Job("1")
result = job()
print(result)

import requests
from lxml import html

class Job:
    
    def __init__(self, typeId):
        self.typeId = typeId

    def call(self):
        items = []
        url = f"https://www.yingshi.tv/vod/show/by/hits_day/id/{self.typeId}/order/desc.html"
        response = requests.get(url)
        tree = html.fromstring(response.content)
        items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[1]/div[2]/div'), "by", "排序", 4))
        items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[1]/div'), "class", "類型", 6))                                             
        items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[2]/div'), "area", "地區", 4))
        items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[3]/div'), "lang", "語言", 8))
        items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[4]/div'), "year", "時間", 10))
        return items

    def filter(self, elements, key, name, index):
        values = []
        for e in elements:
            paragraph = e.xpath('.//p/text()')
            n = paragraph[0] if paragraph else ""
            all_values = "全部" in n
            href = e.xpath('.//a/@href')[0] if not all_values else ""
            v = href.split("/")[-1].replace(".html", "") if href else ""
            values.append({"name": n, "value": v})
        return {"key": key, "name": name, "values": values}

# Example usage:
job = Job("1").call()
print(job)

import requests
from lxml import html
import json

result = {}		
url = 'https://www.yingshi.tv'		
rsp = requests.get(url)
videos = []
root = html.document_fromstring((rsp.text))							
aList = root.xpath('//*[@id="desktop-container"]/section/div/div/li/a') 
for a in aList:
    link = a.xpath("./@href")[0]
    vid = link.split('/')[4]        
    name = (a.xpath('./h2[@class="ys_show_title"]/text()') or [None])[0]
    pic = (a.xpath('./div/img/@src') or [None])[0]
    mark = (a.xpath('.//span[@class="ys_show_episode_text"]/text()') or [None])[0]     
    videos.append({"vod_id": vid, "vod_name": name,"vod_pic": pic,"vod_remarks": mark})            

print(videos)
'''
result = {}
url = 'https://www.yingshi.tv/vod/play/id/200057/sid/1/nid/1.html'
rsp = requests.get(url)
root = html.document_fromstring((rsp.text))
vodData = root.xpath('//script[contains(text(), "let data = ") and contains(text(), "let obj = ")]/text()')[0]
vodData = json.loads(vodData.split('let data = ')[1].split('let obj = ')[0].strip()[:-1].replace("&amp;", " "))
print(vodData['vod_id'])
print(vodData['player_info']['url'])