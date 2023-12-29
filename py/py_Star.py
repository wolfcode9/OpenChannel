#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import requests
import re
from lxml import html

class Spider(Spider):
	apiUrl = "https://aws.ulivetv.net/v3/web/api/filter"
	siteUrl = "https://www.histar.tv/"
	detail = siteUrl + "vod/detail/"
	data = "_next/data/"
	header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": "userIP=127.0.0.1; aws-waf-token=",
        "Referer": siteUrl
    }
	classes = [
		{"type_id": "movie", "type_name": "電影"}, 
		{"type_id": "drama", "type_name": "電視劇"},
		{"type_id": "variety", "type_name": "綜藝"}, 
		{"type_id": "animation", "type_name": "動漫"},
		{"type_id": "documentary", "type_name": "記錄片" }
	]

	def getName(self):
		return "星視界"
	
	def init(self,extend=""):		
		self.extend = extend
	
	def homeContent(self,filter):
		result = {}	
		result['class'] = self.classes
		if self.extend:
			result['filters'] =  self.fetch(self.extend).json()
		return result
	
	def homeVideoContent(self):		
		vod = []
		rsp = self.fetch(self.siteUrl,headers=self.header)		
		tree = self.html(rsp.text)		
		script = self.str2json(self.xpText(tree,'//script[@id="__NEXT_DATA__"]/text()'))
		cards = script["props"]["pageProps"]["cards"]
		for card in cards:
			if card["name"] != "电视直播":
				for v in card['cards']:
					vod.append({
					"vod_id": v['id'],
					"vod_name": v['name'],
					"vod_pic": v['img'],
					"vod_remarks": v['countStr']
				})			
		return	{"list":vod}
	
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		vod = []
		params = {
			"ChName": "电视直播",
			"PageSize": 16,
			"type": extend.get("type", ""),	
			"year": extend.get("year", ""),
			"area": extend.get("area", "")
		}
		rsp = requests.get(url=self.apiUrl,params=params,hasattr=self.header)
		print(rsp.text)
		'''
		jsonData = rsp.json()		
		for v in jsonData['data']['list']:
			vod.append({
				"vod_id": v['id'],
				"vod_name": v['name'],
				"vod_pic": v['picture'],
				"vod_remarks": v['remarks']
			})
		result['list'] = vod
		result['page'] = pg
		result['pagecount'] = jsonData['page']['pageCount']
		result['limit'] = 35
		result['total'] = jsonData['page']['total']
		'''
		return result 
	
	def detailContent(self,array):
		id = array[0]		
		url = self.detail + id
		rsp = self.fetch(url,headers=self.header)
		tree = self.html(rsp.text)		
		script = self.str2json(self.xpText(tree,'//script[@id="__NEXT_DATA__"]/text()'))		
		jsonData = script["props"]["pageProps"]["pageData"]		
		play_urls =  [f'{video["epInfo"]}${video["purl"]}' for video in jsonData["videos"]]
		play_urls = "#".join(play_urls)
		vod = [{
			"vod_id": id,
			"vod_name": jsonData["name"],
			"vod_pic":  jsonData["picurl"],
			"type_name": jsonData["label"],
			"vod_remarks": jsonData["countStr"],
			"vod_year": jsonData["time"],
			"vod_area": jsonData["country"],
			"vod_actor": jsonData["actor"],
			"vod_director": jsonData["director"],
			"vod_content":  jsonData["desc"],
			"vod_play_from" : "wolf",
			"vod_play_url" : play_urls
		}]
		return {"list": vod}
	 
	def searchContent(self,key,quick):
		'''
		#https://m.mubai.link/search?search=我知道我爱你
		result = {}
		url = f"{self.siteUrl}/api/searchFilm?keyword={key}'
		rsp = self.fetch(url)		
		vod = []
		jsonData = rsp.json()
		jsonData = jsonData['data']['list']
		for v in jsonData:
			vod.append({
				"vod_id": v['id'],
				"vod_name": v['name'],
				"vod_pic": v['picture'],
				"vod_remarks": v['remarks']
			})      
		result['list'] = vod
		'''	
		return {}
	
	def playerContent(self,flag,id,vipFlags):
		result = {
        	'parse': '0',
            'playUrl': '',
            'url': id,
            'header': ''
        }
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