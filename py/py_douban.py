#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):

	def getName(self):
		return "熱門影片推薦"
	
	def init(self,extend=""):
		pass	
	
	#主頁
	def homeContent(self,filter):
		result = {}
		return result
	
	#推薦
	def homeVideoContent(self):
		result = {}
		header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
		#最新
		rsp = self.fetch('https://movie.douban.com/j/search_subjects?tag=热门&page_limit=50&page_start=0',headers=header)	
		vData = json.loads(rsp.text)
		vod = []
		for v in vData['subjects']:
			vod.append({
				"vod_id": '',
				"vod_name":v['title'],
				"vod_pic": v['cover'],
				"vod_remarks": v['rate']
			})
		result = {"list":vod}
		return result
	
	#分類
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		return result
	
	#詳情
	def detailContent(self,array):
		result = {}
		return result
	
	#搜索
	def searchContent(self,key,quick):
		result = {}
		return result
	
	#播放
	def playerContent(self,flag,id,vipFlags):
		result = {}
		return result
	
	#視頻格式
	def isVideoFormat(self,url):
		pass
	
	#視頻檢測
	def manualVideoCheck(self):
		pass
	
	#本地代理
	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]