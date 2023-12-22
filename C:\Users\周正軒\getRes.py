import requests
import re
import os
from PIL import Image
from io import BytesIO
import json
import subprocess
import shutil


#下載圖片檔
def download_image(filename, url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(filename)

def getResponseText(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    requests.packages.urllib3.disable_warnings()    
    #response = requests.get(url=url, headers=headers, verify=False, timeout=15)
    response = requests.get(url=url, verify=False, timeout=15)
    response.encoding = 'UTF-8'    
    return response.text
        
'''
#解析YouTube正在直播頻道內容
def getYouTubeLiveInfo(username):    
    response_text = getResponseText(f'https://www.youtube.com/{username}/streams')
    if response_text:
        Q = []
        pattern = re.compile(r'richItemRenderer(.*?)thumbnailOverlays')
        result = re.findall(pattern, response_text)

        #當DEBUG_MODE=True, 將分析資料寫入目錄course記錄歷程,以便查看     
        if DEBUG_MODE:    
            course_file =  f'{COURSE_DIR}\{username}.txt'
            with open(course_file,'w',encoding='utf-8') as file:
                for r in result:
                    file.write(r +'\n\n')            

        for x in result:
            if '正在觀看' in x:
                title = re.search('label(.*?)上傳者：', x).group().split('"')[-1].split(' 上傳者：')[0].replace("\\u0026","&")
                videoId = re.search(f'webCommandMetadata(.*)WEB_PAGE_TYPE_WATCH',x).group().split('=')[1].split('"')[0]       
                viewCount_str = re.search('viewCountText(.*?)正在收看', x).group().split('"')[6].split(' ')[0]
                viewCount = int(viewCount_str.replace(",", ""))
                Q.append({"title": title, "videoId": videoId,'viewCount':viewCount})

        #按照 viewCount 降序排序 (將在線上人數最多的排第一個)
        sorted_Q = sorted(Q, key=lambda x: x['viewCount'], reverse=True)
        return sorted_Q
'''

print(getResponseText(f'http://饭太硬.top/tv'))
   