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
        self.siteUrl = extend
        
    def homeContent(self,filter):
        result = {}
        rsp = self.fetch(f'{self.siteUrl}?ac=list&h=1')
        if rsp:            
            result = {'class:': rsp.json()['class']}
        return result    
        #if(filter):
        #    result['filters'] = self.config['filter']

    def homeVideoContent(self):
        rsp = self.fetch(f'{self.siteUrl}?ac=videolist&h=24')
        if rsp:            
            result = rsp.json()
        return result
    
    def categoryContent(self,tid,pg,filter,extend):   
        result = {}
        url = f'{self.siteUrl}?ac=videolist&t={tid}&pg={pg}'
        rsp = self.fetch(url)
        if rsp:
            result = rsp.json()
        return result

    def detailContent(self,array):
        result = {}
        id = array[0]
        url = f'{self.siteUrl}?ac=videolist&ids={id}'
        rsp = self.fetch(url)
        if rsp:
            result = rsp.json()
        return result

    def searchContent(self,key,quick):
        result = {}        
        patterns = [
            {'keyword': {'kuaikan', 'lziapi'}, 'param': '?ac=videolist&search?text={key}&pg=1'},
            {'keyword': {'bfzyapi', 'ffzyapi'}, 'param': '?ac=videolist&zm={key}&page=1'},
            #{'keyword': {}, 'param': '/list?wd={key}&page=1'},
            #{'keyword': {}, 'param': '?ac=videolist&wd={key}&page=1'},
            #{'keyword': {}, 'param': '?wd={key}&page=1'},
            #{'keyword': {}, 'param': '?wd={key}&page=1'},
        ]
        URL = ""
        for pattern in patterns:
            for keyword in pattern['keyword']:
                if re.search(keyword,self.siteUrl):
                    URL = self.siteUrl + pattern['param'].format(key=key)
                    break
        if URL:
            rsp = self.fetch(URL)
            if rsp:
                result = rsp.json()
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