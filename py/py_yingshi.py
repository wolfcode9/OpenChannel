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
		result['filters'] = self.filter
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

	filter = {'1':[{'key': 'by', 'name': '排序', 'values': [{'n': '新上线', 'v': 'time'}, {'n': '热播榜', 'v': 'hits_day'}, {'n': '好评榜', 'v': 'score'}]}, {'key': 'class', 'name': '類型', 'values': [{'n': '全部类型', 'v': ''}, {'n': '偶像', 'v': '偶像'}, {'n': '爱情', 'v': '爱情'}, {'n': '古装', 'v': '古装'}, {'n': '谍战', 'v': '谍战'}, {'n': '战争', 'v': '战争'}, {'n': '江湖', 'v': '江湖'}, {'n': '武侠', 'v': '武侠'}, {'n': '言情', 'v': '言情'}, {'n': '历史', 'v': '历史'}, {'n': '玄幻', 'v': '玄幻'}, {'n': '历险', 'v': '历险'}, {'n': '都市', 'v': '都市'}, {'n': '科幻', 'v': '科幻'}, {'n': '军旅', 'v': '军旅'}, {'n': '喜剧', 'v': '喜剧'}, {'n': '罪案', 'v': '罪案'}, {'n': '青春', 'v': '青春'}, {'n': '家庭', 'v': '家庭'}, {'n': '悬疑', 'v': '悬疑'}, {'n': '穿越', 'v': '穿越'}, {'n': '宫廷', 'v': '宫廷'}, {'n': '神话', 'v': '神话'}, {'n': '商战', 'v': '商战'}, {'n': '警匪', 'v': '警匪'}, {'n': '动作', 'v': '动作'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '剧情', 'v': '剧情'}, {'n': '同性', 'v': '同性'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '其它', 'v': '其它'}]}, {'key': 'area', 'name': '地區', 'values': [{'n': '全部地区', 'v': ''}, {'n': '大陆', 'v': '大陆'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'}, {'n': '日本', 'v': '日本'}, {'n': '韩国', 'v': '韩国'}, {'n': '欧美', 'v': '欧美'}, {'n': '泰国', 'v': '泰国'}, {'n': '新马', 'v': '新马'}, {'n': '其它', 'v': '其它'}]}, {'key': 'lang', 'name': '語言', 'values': [{'n': '全部语言', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '粤语', 'v': '粤语'}, {'n': '英语', 'v': '英语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '法语', 'v': '法语'}, {'n': '德语', 'v': '德语'}, {'n': '泰语', 'v': '泰语'}, {'n': '其它', 'v': '其它'}]}, {'key': 'year', 'name': '時間', 'values': [{'n': '全部时间', 'v': ''}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90年代'}, {'n': '80年代', 'v': '80年代'}, {'n': '更早', 'v': '更早'}]}]}