from bs4 import BeautifulSoup
import requests

class Vod:
    def __init__(self, id, name, pic, remark):
        self.id = id
        self.name = name
        self.pic = pic
        self.remark = remark

def home_video_content():
    site_url = "https://www.yingshi.tv"
    response = requests.get(site_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    list_of_vod = []

    for e in soup.select('div#desktop-container li.ys_show_item'):
        link = e.select_one('a')['href']
        id = link.split('/')[4]
        pic = e.select_one('img')['src']
        name = e.select_one('h2.ys_show_title')
        remark = e.select_one('span.ys_show_episode_text')

        # 检查name是否为空，然后将结果添加到列表中
        if name:
            vod = Vod(id, name, pic, remark)
            list_of_vod.append(vod)

    return list_of_vod

# 示例用法
result = home_video_content()
for vod in result:
    print(f"ID: {vod.id}, Name: {vod.name}, Pic: {vod.pic}, Remark: {vod.remark}")
