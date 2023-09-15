#!/usr/bin/env python
import requests
import re
import time
from threading import Thread

channelList = [
    {"name":"新聞直播,#genre#"},
    {"name":"東森新聞","key":"東森新聞 51","uid":"@newsebc"},
    {"name":"東森財經","key":"EBC 東森財經新聞","uid":"@57ETFN"},
    {"name":"寰宇新聞","key":"寰宇新聞台 24小時線上直播","uid":"@globalnewstw"},
    {"name":"公共電視","key":"公共電視 13","uid":"@ptslivestream"},
    {"name":"TVBS新聞","key":"TVBS NEWS LIVE","uid":"@TVBSNEWS01"},
    {"name":"中天新聞","key":"CTI中天新聞","uid":"@CtiTv"},
    {"name":"中天亞洲","key":"中天亞洲台","uid":"@CtiAsia"},
    {"name":"台視新聞","key":"台視新聞","uid":"@TTV_NEWS"},
    {"name":"中視新聞","key":"中視新聞","uid":"@twctvnews"},
    {"name":"華視新聞","key":"華視新聞","uid":"@CtsTw"},  
    {"name":"民視新聞","key":"民視新聞","uid":"@FTV_News"},
    {"name":"大愛電視","key":"大愛一臺HD Live","uid":"@DaAiVideo"},
    {"name":"鳳凰衛視","key":"凤凰卫视资讯台24h直播","uid":"@phoenixtvhk"},
    {"name":"中文國際","key":"CCTV中文国际","uid":"@CCTV4International"},
    {"name":"美國新聞","key":"ABC News Live","uid":"@ABCNews"},
    {"name":"日本新聞","key":"JapaNews24","uid":"@ANNnewsCH"},
    {"name":"韓國新聞","key":"YTN","uid":"@ytnnews24"},
    {"name":"新加坡新聞","key":"CNA 24/7 LIVE","uid":"@channelnewsasia"},
    {"name":"德國新聞","key":"Deutsche Welle Live TV","uid":"@dwdeutsch"},
    {"name":"英國新聞","key":"Sky News live","uid":"@SkyNews"},
    {"name":"法國新聞","key":"FRANCE 24 English","uid":"@France24_en"},
    {"name":"德國新聞","key":"DW News livestream","uid":"@dwnews"}, 
    {"name":"歐洲新聞","key":"Euronews English Live","uid":"@euronews"},
    {"name":"音樂串流,#genre#"}, 
    {"name":"流行音樂","key":"網路流行音樂電台","uid":"@2olive153"},
    {"name":"放鬆音樂","key":"治愈壓力","uid":"@lalalandd"},
    {"name":"即時影像,#genre#"},
    {"name":"台中望高寮","key":"台中望高寮4K即時影像","uid":"@user-kc8uj6ro5z"},
    {"name":"台中高美濕地","key":"台中高美濕地4K即時影像","uid":"@user-kc8uj6ro5z"},
    {"name":"桃園石門水庫","key":"石門水庫即時影像","uid":"@TaoyuanTravel"},
    {"name":"南投日月潭","key":"伊達邵碼頭即時影像","uid":"@Itathaosml"},
    {"name":"台北大稻埕","key":"大稻埕碼頭","uid":"@taipeitravelofficial"},
    {"name":"象山看台北","key":"象山看台北","uid":"@taipeitravelofficial"},
    {"name":"台東多良車站","key":"台東多良車站即時影像","uid":"@taitungamazing7249"},    
    {"name":"NASA","key":"NASA Live Stream","uid":"@SpaceVideosHD"}
]

def get_response(html):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url=html, headers=headers)
    response.encoding = 'UTF-8'
    return response.text

def get_youtube_live(uid, index):
    apiUrl = 'https://www.youtube.com/'
    watchUrl = 'https://youtu.be/'
    response_text = get_response(apiUrl + uid)
    data_json = []
    for sp in re.findall('videoRenderer(.*?)viewCountText', response_text):
        text = re.search('label(.*?)上傳者：', sp).group().split('\"')[-1].split('上傳者：')[0]
        videoId = re.search('"videoId(.*?),', sp).group().split('\"')[-2]
        videoUrl = watchUrl + videoId
        iconUrl = re.search('url(.*?).jpg', sp).group().split('\"')[-1]
        data_json.append({'text': text, 'videoUrl': videoUrl, 'iconUrl': iconUrl})
    channelList[index]["text"] = ''
    channelList[index]["videoUrl"] = ''
    channelList[index]["iconUrl"] = ''
    for n in data_json:
        if channelList[index]['key'] in n['text']:
            channelList[index]["text"] = n['text']
            channelList[index]["videoUrl"] = n['videoUrl']
            channelList[index]["iconUrl"] = n['iconUrl']
            break

def process_channels():
    start_time = time.time()
    print('\n解析YouTube直播影片VideoID，取得中...')
    threads = []
    for index, channel in enumerate(channelList):
        if "#genre#" in channel['name']:
            pass
        else:
            thread = Thread(target=get_youtube_live, args=(channel['uid'], index))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    outfile = open('live.txt', 'w', encoding='UTF-8')
    for channel in channelList:
        if "#genre#" in channel['name']:
            outfile.write(channel['name'] + '\n')
        else:
            if channel['videoUrl']:
                outfile.write(channel['name'] + ',' + channel['videoUrl']  + '\n')
            else:                
                print(channel['name'],channel['uid'],channel['key'] + "：●●● 該頻道未找到直播影片! ●●●")

    outfile.close()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'\n檔案\'live.txt\' 寫入完成，執行時間: {elapsed_time:.2f} 秒')

if __name__ == '__main__':
    process_channels()