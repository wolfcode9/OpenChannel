#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):
	
	siteUrl = "https://www.yingshi.tv"
	header = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": siteUrl
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
		classes = []
		cateManual = {
			"電視劇": "1",
			"電影": "2",
			"綜藝": "3",
			"動漫": "4",
			"記錄片": "5"
		}		
		for k in cateManual:
			classes.append({'type_name': k,'type_id': cateManual[k]})

		result['class'] = classes
		return result
	
	#推薦
	def homeVideoContent(self):
		result = {}
		videos = []
		rsp = self.fetch('https://www.yingshi.tv/vod/show/by/time/id/1.html')
		root = self.html(self.cleanText(rsp.text))
		aList = root.xpath('/html/body/div/div/section/div/div/li/a')        
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
	
	#分類
	def categoryContent(self,tid,pg,filter,extend):
		result = {}		
		return result
	
	#詳情
	def detailContent(self,array):
		result = {}
		tid = array[0]
		url = f"{self.siteUrl}/vod/play/id/{tid}/sid/1/nid/1.html"
		rsp = self.fetch(url)
		root = self.html(self.cleanText(rsp.text))
		json_data = root.xpath('//script[contains(text(), "let data = ") and contains(text(), "let obj = ")]/text()')[0]
		json_data = json_data.split('let data = ')[1].split('let obj = ')[0].strip()[:-1].replace("&amp;", " ")
		result = json.loads(json_data)
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