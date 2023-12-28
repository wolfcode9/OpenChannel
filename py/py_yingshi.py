#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import requests

class Spider(Spider):	
	siteUrl = "https://www.yingshi.tv"

	def getName(self):
		return "影視"
	
	def init(self,extend=""):		
		self.extend = extend
	
	def homeContent(self,filter):
		result = {}		
		classes = []		
		cateManual = {
            "電影": "2",
			"電視劇": "1",			
			"綜藝": "3",
			"動漫": "4",
			"記錄片": "5"
		}		
		for k in cateManual:
			classes.append({'type_name': k,'type_id': cateManual[k]})
		result['class'] = classes
		if self.extend:
			rsp = self.fetch(self.extend)
			if rsp.text:
				result['filters'] = self.str2json(rsp.text) 
		return result
	
	def homeVideoContent(self):
		result = {}
		vod = []		
		rsp = self.fetch(self.siteUrl)
		root = self.html(rsp.text)
		if rsp.text:						
			htmlData = root.xpath('//*[@id="desktop-container"]/section/div/div/li/a')       
			for h in htmlData:
				link = h.xpath("./@href")[0]
				vid = link.split('/')[4]
				name = (h.xpath('./h2[@class="ys_show_title"]/text()') or [None])[0]
				pic = (h.xpath('./div/img/@src') or [None])[0]
				mark = (h.xpath('.//span[@class="ys_show_episode_text"]/text()') or [None])[0] 
				if name:
					vod.append({"vod_id": vid, "vod_name": name,"vod_pic": pic,"vod_remarks": mark})					
			result = {'list': vod}
			#另一種很簡單的獲取json,直接取35筆(上限)
			'''		
			url = f'{self.siteUrl}/ajax/data.html?mid=1&limit=35&by=score&order=desc'
			rsp = self.fetch(url)
			vodData = self.str2json(rsp.text)
			result['list'] = vodData['list']
			result = {'list': videos}
			'''
		return result		

	def categoryContent(self,tid,pg,filter,extend):
		#url = f'{self.siteUrl}/ajax/data?mid=1&page={pg}&limit=35&tid={tid}&by=time'		
		result = {}	
		params = {
			"tid": tid,
			"page": pg,
			"limit": "35",
			"mid": "1",
			"by": "time",
			"class": extend.get("class", ""),
			"year": extend.get("year", ""),
			"lang": extend.get("lang", ""),
			"area": extend.get("area", "")			
		}
		url = f'{self.siteUrl}/ajax/data'		
		rsp = requests.get(url=url,params=params)
		if rsp.text:
			vod = []
			jsonData = self.str2json(rsp.text)
			for v in jsonData['list']:
				vod.append({
					"vod_id": v['vod_id'],
					"vod_name": v['vod_name'],
					"vod_pic": v['vod_pic'],
					"vod_remarks": v['vod_remarks']
            	})			
			result['list'] = vod
			result['page'] = pg
			result['pagecount'] = jsonData['pagecount']
			result['limit'] = 35
			result['total'] = jsonData['total']
		return result 
	
	def detailContent(self,array):
		result = {}
		tid = array[0]
		url = f"{self.siteUrl}/vod/play/id/{tid}/sid/1/nid/1.html"
		rsp = self.fetch(url)
		if rsp.text:			
			root = self.html(rsp.text)
			htmlData = root.xpath('//script[contains(text(), "let data = ") and contains(text(), "let obj = ")]/text()')[0]
			vod = self.str2json(htmlData.split('let data = ')[1].split('let obj = ')[0].strip()[:-1].replace("&amp;", " "))
			result = {'list': [{
				"vod_id": vod['vod_id'],
				"vod_name": vod['vod_name'],
				"vod_pic": vod['vod_pic'],
				"vod_remarks": vod['vod_remarks'],
				"type_name": vod['type']['type_name'],
				"vod_year": vod['vod_year'],
				"vod_area": vod['vod_area'],
				"vod_actor": vod['vod_actor'],
				"vod_director": vod['vod_director'],
				"vod_content": vod['vod_content'],
				"vod_play_from": vod['vod_play_from'],
				"vod_play_url": vod['vod_play_url']
			}]}			
		return result
	
	def searchContent(self,key,quick):		
		result = {}
		url = f'{self.siteUrl}/ajax/search.html?wd={key}&mid=1&limit=18&page=1'
		rsp = self.fetch(url)
		if rsp.text:
			jsonData = self.str2json(rsp.text)
			result['list'] = jsonData['list']
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