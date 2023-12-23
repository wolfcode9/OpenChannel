# coding=utf-8
# !/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import base64
from Crypto.Cipher import AES
import json
import requests

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
