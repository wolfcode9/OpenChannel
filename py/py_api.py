#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    siteUrl = ""

    def getName(self):
        return "影視Api"
    
    def init(self,extend=""):
        self.siteUrl = extend
        
    def homeContent(self,filter):
        #https://bfzyapi.com/api.php/provide/vod?ac=list&h=1
        result = {}
        vodList = self.fetch(f'{self.siteUrl}?ac=list&h=1').json()
        result['class'] = vodList['class']        
        #if(filter):
        #    result['filters'] = self.config['filter']s
        return result

    def homeVideoContent(self):
        #https://bfzyapi.com/api.php/provide/vod?ac=detail&h=24
        vodList = self.fetch(f'{self.siteUrl}?ac=detail&h=24').json()
        return {'list': vodList['list']}
    
    def categoryContent(self,tid,pg,filter,extend):
        result = {}
        #params = '&'.join([f'{key}={extend[key]}' for key in extend])        
        #url = f'{self.siteUrl}??ac=list&t={{tid}}&pg={pg}&{params}'
        url = f'{self.siteUrl}?ac=detail&t={tid}&pg={pg}'
        vodList = self.fetch(url).json()
        result['list'] = vodList['list']
        result['page'] = pg
        result['pagecount'] = vodList['pagecount']
        result['limit'] = vodList['limit']
        result['total'] = vodList['total']
        return result

    def detailContent(self,array):
        id = array[0]
        url = f'{self.siteUrl}?ac=detail&ids={id}'
        vodList = self.fetch(url).json()        
        return {'list': vodList['list']}

    def searchContent(self,key,quick):
        url = f'{self.siteUrl}?ac=detail&wd={key}'
        vodList = self.fetch(url).json()        
        return {'list': vodList['list']}

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
