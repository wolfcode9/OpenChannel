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
		filters = []	
		cateManual = {
			"電視劇": "1",
			"電影": "2",
			"綜藝": "3",
			"動漫": "4",
			"記錄片": "5"
		}		
		for k in cateManual:
			classes.append({'type_name': k,'type_id': cateManual[k]})
			filters.append({cateManual[k]:self.job(cateManual[k])})

		result['class'] = classes	
		result['filters'] = filters
		return result
	
	#推薦頁
	def homeVideoContent(self):
		result = {}
		videos = []		
		rsp = self.fetch(self.siteUrl)
		root = self.html(rsp.text)
		if rsp.text:						
			aList = root.xpath('//*[@id="desktop-container"]/section/div/div/li/a')       
			for a in aList:
				link = a.xpath("./@href")[0]
				vid = link.split('/')[4]
				name = (a.xpath('./h2[@class="ys_show_title"]/text()') or [None])[0]
				pic = (a.xpath('./div/img/@src') or [None])[0]
				mark = (a.xpath('.//span[@class="ys_show_episode_text"]/text()') or [None])[0] 
				if name:
					videos.append({"vod_id": vid, "vod_name": name,"vod_pic": pic,"vod_remarks": mark})					
			result = {'list': videos}
			#另一種很簡單的獲取json,直接取35筆(上限)
			'''		
			url = f'{self.siteUrl}/ajax/data.html?mid=1&limit=35&by=score&order=desc'
			rsp = self.fetch(url)
			vodData = json.loads(rsp.text)
			result['list'] = vodData['list']
			result = {'list': videos}
			'''
		return result		

	#分類
	def categoryContent(self,tid,pg,filter,extend):
		result = {}		
		url = f'{self.siteUrl}/ajax/data?mid=1&page={pg}&limit=35&tid={tid}&by=time'		
		rsp = self.fetch(url)
		if rsp.text:
			vodData = json.loads(rsp.text)
			result['list'] = vodData['list']
			result['page'] = pg
			result['pagecount'] = vodData['pagecount']
			result['limit'] = 35
			result['total'] = vodData['total']
		return result 
	
	#詳情
	def detailContent(self,array):
		result = {}
		tid = array[0]
		url = f"{self.siteUrl}/vod/play/id/{tid}/sid/1/nid/1.html"
		rsp = self.fetch(url)
		if rsp.text:			
			root = self.html(rsp.text)
			vodData = root.xpath('//script[contains(text(), "let data = ") and contains(text(), "let obj = ")]/text()')[0]
			vodData = json.loads(vodData.split('let data = ')[1].split('let obj = ')[0].strip()[:-1].replace("&amp;", " "))
			result = {'list': [vodData]}
		return result
	
	#搜索
	def searchContent(self,key,quick):		
		result = {}
		url = f'{self.siteUrl}/ajax/search.html?wd={key}&mid=1&limit=18&page=1'
		rsp = self.fetch(url)
		if rsp.text:
			vodData = json.loads(rsp.text)
			result['list'] = vodData['list']
		return result
	
	#播放	
	def playerContent(self,flag,id,vipFlags):
		result = {
        	'parse': '0',
            'playUrl': '',
            'url': id,
            'header': ''
        }
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

	def job(self, typeId):
		items = []
		url = f"https://www.yingshi.tv/vod/show/by/hits_day/id/{typeId}/order/desc.html"
		rsp = self.fetch(url)
		tree = self.html(rsp.text)
		items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[1]/div[2]/div'), "by", "排序", 4))
		items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[1]/div'), "class", "類型", 6))                                             
		items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[2]/div'), "area", "地區", 4))
		items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[3]/div'), "lang", "語言", 8))
		items.append(self.filter(tree.xpath('/html/body/div[5]/div/div[2]/div[2]/div[4]/div'), "year", "時間", 10))
		return items

	def filter(self, elements, key, name, index):
		values = []
		for e in elements:
			paragraph = e.xpath('.//p/text()')
			n = paragraph[0] if paragraph else ""
			all_values = "全部" in n
			href = e.xpath('.//a/@href')[0] if not all_values else ""
			v = href.split("/")[-1].replace(".html", "") if href else ""
			values.append({"n": n, "v": v})
		return {"key": key, "name": name, "values": values}