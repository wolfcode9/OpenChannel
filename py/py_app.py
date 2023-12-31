#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import re

class Spider(Spider):    

    def getName(self):
        return "影視App"
    
    def init(self,extend=""):
        self.siteUrl = "https://bfzyapi.com/api.php/provide/vod" #extend
        # "https://kuaikan-api.com/api.php/provide/vod/from/kuaikan"         
        
    def homeContent(self,filter):
        # https://bfzyapi.com/api.php/provide/vod?ac=list&h=1
        result = {}
        vodList = self.fetch(f'{self.siteUrl}?ac=list&h=1').json()
        result['class'] = vodList['class']        
        #if(filter):
        #    result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        # https://bfzyapi.com/api.php/provide/vod?ac=detail&h=24
        vodList = self.fetch(f'{self.siteUrl}?ac=videolist&h=24').json()
        return {'list': vodList['list']}
    
    def categoryContent(self,tid,pg,filter,extend):
        result = {}
        # https://kuaikan-api.com/api.php/provide/vod/from/kuaikan?ac=videolist&t=1&pg=1
        #params = '&'.join([f'{key}={extend[key]}' for key in extend])        
        #url = f'{self.siteUrl}??ac=list&t={{tid}}&pg={pg}&{params}'
        url = f'{self.siteUrl}?ac=videolist&t={tid}&pg={pg}'
        vodList = self.fetch(url).json()
        result['list'] = vodList['list']
        result['page'] = pg
        result['pagecount'] = vodList['pagecount']
        result['limit'] = vodList['limit']
        result['total'] = vodList['total']
        return result

    def detailContent(self,array):
        id = array[0]
        url = f'{self.siteUrl}?ac=videolist&ids={id}'
        vodList = self.fetch(url).json()        
        return {'list': vodList['list']}

    def searchContent(self,key,quick):
        result = {}
        H = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Host": "kuaikan-api.com",
            "Referer" : "https://kuaikan-api.com"
        }
        params = {
            'param1': '?ac=videolist&search?text={key}&pg=1',
            'param2': '?ac=videolist&zm={key}&page=1',        
            #'param2': '/list?wd={key}&page=1',
            #'param3': '?wd={key}&page=1',
            #'param4': '?ac=videolist&wd={key}&page=1',
            #'param5': '?ac=videolist&zm={key}&page=1'
        }
        patterns = {
            'pattern1': re.compile(r'kuaikan|lziapi'),
            'pattern2': re.compile(r'bfzyapi'),
            #'pattern3': re.compile(r''),
            #'pattern4': re.compile(r''),
            #'pattern5': re.compile(r'')
        }
        URL = ""        
        for index, pattern in patterns.items():
            if pattern.search(self.siteUrl):
                URL = self.siteUrl + params[f'param{index[-1]}'].format(key=key)
                print(URL)            
                break
        if URL:
            vodList = self.fetch(URL).json()
            result = {'list': vodList['list']}            
        return result  

    def playerContent(self,flag,id,vipFlags):
        result = {}        
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        return result
    
    def isVideoFormat(self,url):
        pass

    def manualVideoCheck(self):
        pass

    def localProxy(self,param):
        action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
        return [200, "video/MP2T", action, ""]