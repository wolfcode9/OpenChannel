#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json

class Spider(Spider):
	
	siteUrl = "https://m.mubai.link/"
	header = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": siteUrl
	}	

	def getName(self):
		return "孟買"
	
	def init(self,extend=""):
		self.extend = extend
	
	#主頁
	def homeContent(self,filter):
		#<a data-v-b4028804="" href="/filmClassify?Pid=1">电影</a>
		result = {}		
		classes = []		
		cateManual = {
			"電影": "1",
			"劇集": "2",
			"綜藝": "3",
			"動漫": "4"			
		}		
		for k in cateManual:
			classes.append({'type_name': k,'type_id': cateManual[k]})			

		result['class'] = classes
		'''
		if self.extend:
			rsp = self.fetch(self.extend)
			if rsp.text:
				result['filters'] = json.loads(rsp.text)
		'''
		return result
	
	#推薦頁
	def homeVideoContent(self):
		result = {}
		videos = []
		return result		
		'''
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
			
			url = f'{self.siteUrl}/ajax/data.html?mid=1&limit=35&by=score&order=desc'
			rsp = self.fetch(url)
			vodData = json.loads(rsp.text)
			result['list'] = vodData['list']
			result = {'list': videos}
			'''

	#分類
	def categoryContent(self,tid,pg,filter,extend):
		#https://m.mubai.link/filmClassifySearch?Pid=1&Sort=update_stamp&current=1
		result = {}	
		videos = []	
		url = f'{self.siteUrl}/api/filmClassifySearch?Pid={tid}&Sort=update_stamp&current={pg}'
		rsp = self.fetch(url)
		if rsp.text:
			vodData = json.loads(rsp.text)
			for vod in vodData['data']['list']:
				videos.append({
					"vod_id": vod['id'],
					"vod_name": vod['name'],
					"vod_pic": vod['picture'],
					"vod_remarks": vod['remarks']
            	})
			result['list'] = videos
			result['page'] = pg
			result['pagecount'] = vodData['page']['pageCount']
			result['limit'] = 35
			result['total'] = vodData['page']['total']
		return result 
	
	#詳情
	def detailContent(self,array):
		#https://m.mubai.link/api/filmDetail?id=77886
		result = {}		
		id = array[0]
		url = f"{self.siteUrl}/api/filmDetail?id={id}"
		rsp = self.fetch(url)
		if rsp.text:
			playUrls = []			
			vodeos = []
			vodData = json.loads(rsp.text)
			vodData = vodData['data']['detail']			
			for v in vodData['playList'][0]:				
				playUrls.append('#'.join([v['episode'] + '$' + v['link']]))

			vodeos.append ({
				"vod_id": id,
				"vod_name": vodData['name'],
				"vod_pic":  vodData['picture'],
				"type_name": vodData['descriptor']['classTag'],
				"vod_remarks": vodData['descriptor']['remarks'],
				"vod_year": vodData['descriptor']['year'],
				"vod_area": vodData['descriptor']['area'],
				"vod_actor": vodData['descriptor']['actor'],
				"vod_director": vodData['descriptor']['director'],
				"vod_content": vodData['descriptor']['content'],
				"vod_play_from" : 'liangzi', #'$$$'.join(vodData['playFrom']),			
				"vod_play_url" : '$$$'.join(playUrls)
				})
			result['list'] = vodeos
		return result	
	 
	#搜索
	def searchContent(self,key,quick):
		#https://m.mubai.link/search?search=我知道我爱你
		result = {}
		url = f'{self.siteUrl}/api/searchFilm?keyword={key}'
		rsp = self.fetch(url)
		if rsp.text:
			videos = []
			vodData = json.loads(rsp.text)
			vodData = vodData['data']['list']
			for v in vodData:
				videos.append({
					"vod_id": v['id'],
					"vod_name": v['name'],
					"vod_pic": v['picture'],
					"vod_remarks": v['remarks']
				})      
			result['list'] = videos
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

'''
debug = 1
if debug:
	from pprint import pprint
	sp = Spider()
	match debug:
		case 1:
			pprint(sp.detailContent(['78594']))
		case 2:			
			pprint(sp.searchContent('三大',''))
		
		case _:
			pass	

'''