#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):

	def getName(self):
		return "豆瓣薦片"
	
	def init(self,extend=""):
		pass	
	
	def homeContent(self,filter):
		result = {}
		return result
	
	#推薦頁面
	def homeVideoContent(self):
		result = {}
		header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
		#電視劇 https://movie.douban.com/j/search_subjects?type=tv&tag=热门&page_limit=50
		#電影 https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=50
		rsp = self.fetch('https://movie.douban.com/j/search_subjects?type=tv&tag=热门&page_limit=50',headers=header)	
		vData = json.loads(rsp.text)
		vod = []
		
		for v in vData['subjects']:
			remarks = v['episodes_info'] or v['rate']
			vod.append({
				"vod_name": v['title'],
				"vod_pic": v['cover'],
				"vod_remarks": remarks
			})
		result = {"list":vod}
		return result
	
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		return result
	
	def detailContent(self,array):
		result = {}
		return result
	
	def searchContent(self,key,quick):
		result = {}
		return result
	
	def playerContent(self,flag,id,vipFlags):
		result = {}
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