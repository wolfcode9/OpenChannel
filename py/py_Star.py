#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import requests
import urllib.parse
import json

class Spider(Spider):
	apiUrl = "https://aws.ulivetv.net/v3/web/api/filter"
	siteUrl = "https://www.histar.tv/"
	detail = siteUrl + "vod/detail/"
	data = "_next/data/"
	ver = ""
	header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": "userIP=127.0.0.1; aws-waf-token=",
        "Referer": siteUrl
    }
	classes = [
		{"type_id": "movie", "type_name": "电影"}, 
		{"type_id": "drama", "type_name": "电视剧"},
		{"type_id": "variety", "type_name": "综艺"}, 
		{"type_id": "animation", "type_name": "动漫"},
		{"type_id": "documentary", "type_name": "纪录片"}
	]	

	def getName(self):
		return "星視界"
	
	def init(self,extend=""):
		self.extend = extend
		self.ver = self.getVer()
	
	def homeContent(self,filter):
		result = {}	
		f = []
		result['class'] = self.classes
		'''
		for cls in self.classes:
			url = self.siteUrl + cls["type_id"] + "/all/all/all"
			rsp = self.fetch(url,headers=self.header)
			tree = self.html(rsp.text)			
			script = self.str2json(self.xpText(tree,'//script[@id="__NEXT_DATA__"]/text()'))
			f.append(script["props"]["pageProps"]["filterCondition"]["label"])
        #if self.extend:
		result['filters'] =  f #self.fetch(self.extend).json()
		'''
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
		cnName = next(cls["type_name"] for cls in self.classes if cls["type_id"] == tid)		
		query = {
    		"chName":cnName,
    		"pageSize":16,
    		"page":pg,
            "year": extend.get("year", ""),
            "type": extend.get("type", ""),
            "area": extend.get("area", "")
		}	
		jsonData = requests.post(url=self.apiUrl,json=query,headers=self.header).json()		 
		vod = []
		for v in jsonData['data']['list']:
			vod.append({
				"vod_id": v['id'],
				"vod_name": v['name'],
				"vod_pic": v['img'],
				"vod_remarks": v['countStr']
        })
		result['list'] = vod
		result['page'] = pg
		result['pagecount'] = jsonData['data']['pageSize']
		result['limit'] = 35
		result['total'] = jsonData['data']['total']		
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
		url = f"{self.siteUrl}{self.data}{self.ver}/search.json?word={urllib.parse.quote(key)}"
		jsonData = self.fetch(url,headers=self.header).json()
		vod = []		
		jsonData = jsonData['pageProps']['initList']
		for v in jsonData:
			vod.append({
				"vod_id": v['id'],
				"vod_name": v['name'],
				"vod_pic": v['picurl'],
				"vod_remarks": v['countStr']
			})			
		return {"list" : vod}
	
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
	
	def getVer(self):    
		rsp = self.fetch(self.siteUrl,headers=self.header)
		tree = self.html(rsp.text)			
		ver = tree.xpath('//script[contains(@src, "_buildManifest.js")]/@src')[0]
		ver = ver.split("/")[3]
		return ver
		