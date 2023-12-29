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
		result = {}
		vod = []
		rsp = self.fetch(self.siteUrl,headers=self.header)		
		tree = self.html(rsp.text)		
		script = self.str2json(self.xpText(tree,'//script[@id="__NEXT_DATA__"]/text()'))
		cards = script["props"]["pageProps"]["cards"]
		for card in cards:
			if card["name"] != "电视直播":
				vod += card["cards"]
		result['list'] = vod
		
		'''
		for c in self.classes:
			url = f'{self.siteUrl}{c["type_id"]}/all/all/all'
			rsp = self.fetch(url,headers=self.header)			
			tree = self.html(rsp.text)
			script_data = self.xpText(tree,'//script[@id="__NEXT_DATA__"]')
			print(script_data)
		
		
		vod = []
		jsonData = rsp.json()
		for content in jsonData['data']['content']:
			for v in content['movies']:
				vod.append({
					"vod_id": v['id'],
					"vod_name": v['name'],
					"vod_pic": v['picture'],
					"vod_remarks": v['remarks']
				})
		result['list'] = vod
		'''
		return result
	
	def categoryContent(self,tid,pg,filter,extend):
		return {}
		#https://m.mubai.link/filmClassifySearch?Pid=1&Sort=release_stamp&current=1
		result = {}	
		vod = []			
		params = {
			"Pid": tid,
			"current": pg,
			"Sort": extend.get("Sort", "release_stamp"),
			"Category": extend.get("Category", ""),
			"Plot": extend.get("Plot", ""),			
			"Year": extend.get("Year", ""),
			"Language": extend.get("Language", ""),
			"Area": extend.get("Area", "")
		}
		url = f'{self.siteUrl}/api/filmClassifySearch'
		rsp = requests.get(url=url,params=params)

		if rsp.text:
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
		return result 
	
	def detailContent(self,array):
		return {}
		#https://m.mubai.link/api/filmDetail?id=77886
		result = {}		
		id = array[0]
		url = f"{self.siteUrl}/api/filmDetail?id={id}"
		rsp = self.fetch(url)
		if rsp.text:
			playUrls = []			
			vod = []
			jsonData = rsp.json()
			jsonData = jsonData['data']['detail']			
			for v in jsonData['playList'][0]:				
				playUrls.append('#'.join([v['episode'] + '$' + v['link']]))
			cleaned_content = re.sub(r'<p>\s*|\s*</p>', '', jsonData['descriptor']['content'])			
			vod.append ({
				"vod_id": id,
				"vod_name": jsonData['name'],
				"vod_pic":  jsonData['picture'],
				"type_name": jsonData['descriptor']['classTag'],
				"vod_remarks": jsonData['descriptor']['remarks'],
				"vod_year": jsonData['descriptor']['year'],
				"vod_area": jsonData['descriptor']['area'],
				"vod_actor": jsonData['descriptor']['actor'],
				"vod_director": jsonData['descriptor']['director'],
				"vod_content": cleaned_content,
				"vod_play_from" : 'liangzi',
				"vod_play_url" : '#'.join(playUrls)
				})			
			result['list'] = vod
		return result	
	 
	def searchContent(self,key,quick):
		return {}
		#https://m.mubai.link/search?search=我知道我爱你
		result = {}
		url = f'{self.siteUrl}/api/searchFilm?keyword={key}'
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
		return result
	
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