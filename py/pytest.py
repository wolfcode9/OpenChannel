from base.spider import Spider
from lxml import html

url = "https://www.yingshi.tv/vod/show/by/time/id/1.html"

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