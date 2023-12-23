from base.spider import Spider
from lxml import html

url = "https://www.yingshi.tv/vod/show/by/time/id/1.html"

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
'''

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
