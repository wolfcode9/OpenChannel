#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):
	
	siteUrl = ''
	header = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer":  siteUrl
	}
	config = {
		"player": {},
		"filter": {}
	}

	def getName(self):
		return "影視"
	
	def init(self,extend=""):
		pass
	
	#主頁
	def homeContent(self,filter):
		result = {}
		return result
	
	#推薦
	def homeVideoContent(self):
		result = {}
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