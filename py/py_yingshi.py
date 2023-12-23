# coding=utf-8
# !/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import base64
from Crypto.Cipher import AES
import json
import requests
from bs4 import BeautifulSoup
from typing import List

class Spider(Spider):    
    siteUrl = "https://www.yingshi.tv"
    headers = {	
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.yingshi.tv"
    }

    def getName(self):
        return "影視"

    def init(self, extend=""):        
        pass
    
    #https://www.yingshi.tv/vod/show/by/time/id/5.html
    def homeContent(self,filter):
        result = {}
        cateManual = {
            "電視劇": "1",
            "電影": "2",
            "綜藝": "3",
            "動漫": "4",
            "記錄片": "5"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes        
        #if(filter):
        #    result['filters'] = self.config
        return result

    def homeVideoContent(self):
        rsp = self.fetch('https://www.yingshi.tv/vod/show/by/time/id/1.html')
        root = self.html(self.cleanText(rsp.text))
        aList = root.xpath('/html/body/div/div/section/div/div/li/a')        
        videos = []
        for a in aList:
            link = a.xpath("./@href")[0]            
            vid = link.split('/')[4]        
            name = (a.xpath('./h2[@class="ys_show_title"]/text()') or [None])[0]
            pic = (a.xpath('./div/img/@src') or [None])[0]
            mark = (a.xpath('.//span[@class="ys_show_episode_text"]/text()') or [None])[0] 
            if name:
                videos.append({"vod_id": vid, "vod_name": name,"vod_pic": pic,"vod_remarks": mark})            
        result = {'list': videos}
        return result

    def categoryContent(self, tid, pg, filter, extend):
        extend = {
            "by": "time" if "by" not in extend else extend["by"],
            "class": "" if "class" not in extend else extend["class"],
            "area": "" if "area" not in extend else extend["area"],
            "lang": "" if "lang" not in extend else extend["lang"],
            "year": "" if "year" not in extend else extend["year"]
        }
        params = {
            "mid": "1",
            "by": extend["by"],
            "tid": tid,
            "page": pg,
            "class": extend["class"],
            "year": extend["year"],
            "lang": extend["lang"],
            "area": extend["area"],
            "limit": "35"
        }
        url = f'{self.siteUrl}/ajax/data'
        return requests.get(url,params=params, headers=self.headers)    

    def detailContent(self, array):
        tid = array[0]
        url = f"{self.siteUrl}/vod/play/id/{tid}/sid/1/nid/1.html"
        rsp = self.fetch(url)
        root = self.html(self.cleanText(rsp.text))
        json_data = root.xpath('//script[contains(text(), "let data = ") and contains(text(), "let obj = ")]/text()')[0]
        json_data = json_data.split('let data = ')[1].split('let obj = ')[0].strip()[:-1].replace("&amp;", " ")
        vod = json.loads(json_data)
        return str(vod)

    def searchContent(self, key, quick):        
        url = 'https://www.czzy88.com/xssearch?q={0}'.format(key)
        rsp = self.fetch(url,headers=header)
        root = self.html(self.cleanText(rsp.text))
        vodList = root.xpath("//div[contains(@class,'mi_ne_kd')]/ul/li/a")
        videos = []
        for vod in vodList:
            name = vod.xpath('./img/@alt')[0]
            pic = vod.xpath('./img/@data-original')[0]
            href = vod.xpath('./@href')[0]
            tid = self.regStr(href, 'movie/(\\S+).html')
            res = vod.xpath('./div[@class="jidi"]/span/text()')
            if len(res) == 0:
                remark = '全1集'
            else:
                remark = vod.xpath('./div[@class="jidi"]/span/text()')[0]
            videos.append({
                "vod_id": tid,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            })
        result = {
            'list': videos
        }
        return result    

    def parseCBC(self, enc, key, iv):
        keyBytes = key.encode("utf-8")
        ivBytes = iv.encode("utf-8")
        cipher = AES.new(keyBytes, AES.MODE_CBC, ivBytes)
        msg = cipher.decrypt(enc)
        paddingLen = msg[len(msg) - 1]
        return msg[0:-paddingLen]
    
    #https://www.yingshi.tv/vod/play/id/198804/sid/1/nid/1.html
    def playerContent(self, flag, id, vipFlags):
        url = self.siteUrl + '/vod/play/id/{0}/sid/1/nid/1.html'.format(id)
        pat = '\\"([^\\"]+)\\";var [\\d\\w]+=function dncry.*md5.enc.Utf8.parse\\(\\"([\\d\\w]+)\\".*md5.enc.Utf8.parse\\(([\\d]+)\\)'
        rsp = self.fetch(url)
        html = rsp.text
        content = self.regStr(html, pat)
        if content == '':
            return {}
        key = self.regStr(html, pat, 2)
        iv = self.regStr(html, pat, 3)
        decontent = self.parseCBC(base64.b64decode(content), key, iv).decode()
        urlPat = 'video: \\{url: \\\"([^\\\"]+)\\\"'
        vttPat = 'subtitle: \\{url:\\\"([^\\\"]+\\.vtt)\\\"'
        str3 = self.regStr(decontent, urlPat)
        str4 = self.regStr(decontent, vttPat)
        self.loadVtt(str3)
        result = {
            'parse': '0',
            'playUrl': '',
            'url': str3,
            'header': ''
        }
        if len(str4) > 0:
            result['subf'] = '/vtt/utf-8'
            # result['subt'] = Proxy.localProxyUrl() + "?do=czspp&url=" + URLEncoder.encode(str4)
            result['subt'] = ''
        return result

    def loadVtt(self, url):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def localProxy(self, param):
        action = {}
        return [200, "video/MP2T", action, ""]

    config = {[  
    {
        "key": "by",
        "name": "排序",
        "values": [
        {
            "name": "新上线",
            "value": "time"
        },
        {
            "name": "热播榜",
            "value": "hits_day"
        },
        {
            "name": "好评榜",
            "value": "score"
        }
        ]
    },
    {
        "key": "class",
        "name": "類型",
        "values": [
        {
            "name": "全部类型",
            "value": ""
        },
        {
            "name": "偶像",
            "value": "偶像"
        },
        {
            "name": "爱情",
            "value": "爱情"
        },
        {
            "name": "古装",
            "value": "古装"
        },
        {
            "name": "谍战",
            "value": "谍战"
        },
        {
            "name": "战争",
            "value": "战争"
        },
        {
            "name": "江湖",
            "value": "江湖"
        },
        {
            "name": "武侠",
            "value": "武侠"
        },
        {
            "name": "言情",
            "value": "言情"
        },
        {
            "name": "历史",
            "value": "历史"
        },
        {
            "name": "玄幻",
            "value": "玄幻"
        },
        {
            "name": "历险",
            "value": "历险"
        },
        {
            "name": "都市",
            "value": "都市"
        },
        {
            "name": "科幻",
            "value": "科幻"
        },
        {
            "name": "军旅",
            "value": "军旅"
        },
        {
            "name": "喜剧",
            "value": "喜剧"
        },
        {
            "name": "罪案",
            "value": "罪案"
        },
        {
            "name": "青春",
            "value": "青春"
        },
        {
            "name": "家庭",
            "value": "家庭"
        },
        {
            "name": "悬疑",
            "value": "悬疑"
        },
        {
            "name": "穿越",
            "value": "穿越"
        },
        {
            "name": "宫廷",
            "value": "宫廷"
        },
        {
            "name": "神话",
            "value": "神话"
        },
        {
            "name": "商战",
            "value": "商战"
        },
        {
            "name": "警匪",
            "value": "警匪"
        },
        {
            "name": "动作",
            "value": "动作"
        },
        {
            "name": "惊悚",
            "value": "惊悚"
        },
        {
            "name": "剧情",
            "value": "剧情"
        },
        {
            "name": "同性",
            "value": "同性"
        },
        {
            "name": "奇幻",
            "value": "奇幻"
        },
        {
            "name": "其它",
            "value": "其它"
        }
        ]
    },
    {
        "key": "area",
        "name": "地區",
        "values": [
        {
            "name": "全部地区",
            "value": "全部地区"
        },
        {
            "name": "大陆",
            "value": "大陆"
        },
        {
            "name": "香港",
            "value": "香港"
        },
        {
            "name": "台湾",
            "value": "台湾"
        },
        {
            "name": "日本",
            "value": "日本"
        },
        {
            "name": "韩国",
            "value": "韩国"
        },
        {
            "name": "欧美",
            "value": "欧美"
        },
        {
            "name": "泰国",
            "value": "泰国"
        },
        {
            "name": "新马",
            "value": "新马"
        },
        {
            "name": "其它",
            "value": "其它"
        }
        ]
    },
    {
        "key": "lang",
        "name": "語言",
        "values": [
        {
            "name": "全部语言",
            "value": "全部语言"
        },
        {
            "name": "国语",
            "value": "国语"
        },
        {
            "name": "粤语",
            "value": "粤语"
        },
        {
            "name": "英语",
            "value": "英语"
        },
        {
            "name": "韩语",
            "value": "韩语"
        },
        {
            "name": "日语",
            "value": "日语"
        },
        {
            "name": "西班牙",
            "value": "西班牙"
        },
        {
            "name": "法语",
            "value": "法语"
        },
        {
            "name": "德语",
            "value": "德语"
        },
        {
            "name": "泰语",
            "value": "泰语"
        },
        {
            "name": "其它",
            "value": "其它"
        }
        ]
    },
    {
        "key": "year",
        "name": "時間",
        "values": [
        {
            "name": "全部时间",
            "value": "全部时间"
        },
        {
            "name": "2023",
            "value": "2023"
        },
        {
            "name": "2022",
            "value": "2022"
        },
        {
            "name": "2021",
            "value": "2021"
        },
        {
            "name": "2020",
            "value": "2020"
        },
        {
            "name": "2019",
            "value": "2019"
        },
        {
            "name": "2018",
            "value": "2018"
        },
        {
            "name": "2017",
            "value": "2017"
        },
        {
            "name": "2016",
            "value": "2016"
        },
        {
            "name": "2015",
            "value": "2015"
        },
        {
            "name": "2014-2011",
            "value": "2014-2011"
        },
        {
            "name": "2010-2000",
            "value": "2010-2000"
        },
        {
            "name": "90年代",
            "value": "90年代"
        },
        {
            "name": "80年代",
            "value": "80年代"
        },
        {
            "name": "更早",
            "value": "更早"
        }
        ]
    }
    ]}

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
                values.append({"name": n, "value": v})
        return {"key": key, "name": name, "values": values}

   