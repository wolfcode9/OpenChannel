#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):    

    def getName(self):
        return "Wolf"
    
    def init(self,extend=""):
        self.siteUrl = extend
        
    def homeContent(self,filter):
        result = {}
        rsp = self.fetch(f'{self.siteUrl}?ac=list&h=1')
        if rsp:            
            result = {'class': rsp.json()['class']}
        return result

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
        url = f'{self.siteUrl}?ac=videolist&wd={key}&page=1'
        rsp = self.fetch(url)
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