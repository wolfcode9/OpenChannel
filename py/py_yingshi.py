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
		"filter": {"1":[{'key': 'by', 'name': '排序', 'values': [{'n': '新上线', 'v': 'time'}, {'n': '热播榜', 'v': 'hits_day'}, {'n': '好评榜', 'v': 'score'}]}, {'key': 'class', 'name': '類型', 'values': [{'n': '全部类型', 'v': ''}, {'n': '偶像', 'v': '%E5%81%B6%E5%83%8F'}, {'n': '爱情', 'v': '%E7%88%B1%E6%83%85'}, {'n': '古装', 'v': '%E5%8F%A4%E8%A3%85'}, {'n': '谍战', 'v': '%E8%B0%8D%E6%88%98'}, {'n': '战争', 'v': '%E6%88%98%E4%BA%89'}, {'n': '江湖', 'v': '%E6%B1%9F%E6%B9%96'}, {'n': '武侠', 'v': '%E6%AD%A6%E4%BE%A0'}, {'n': '言情', 'v': '%E8%A8%80%E6%83%85'}, {'n': '历史', 'v': '%E5%8E%86%E5%8F%B2'}, {'n': '玄幻', 'v': '%E7%8E%84%E5%B9%BB'}, {'n': '历险', 'v': '%E5%8E%86%E9%99%A9'}, {'n': '都市', 'v': '%E9%83%BD%E5%B8%82'}, {'n': '科幻', 'v': '%E7%A7%91%E5%B9%BB'}, {'n': '军旅', 'v': '%E5%86%9B%E6%97%85'}, {'n': '喜剧', 'v': '%E5%96%9C%E5%89%A7'}, {'n': '罪案', 'v': '%E7%BD%AA%E6%A1%88'}, {'n': '青春', 'v': '%E9%9D%92%E6%98%A5'}, {'n': '家庭', 'v': '%E5%AE%B6%E5%BA%AD'}, {'n': '悬疑', 'v': '%E6%82%AC%E7%96%91'}, {'n': '穿越', 'v': '%E7%A9%BF%E8%B6%8A'}, {'n': '宫廷', 'v': '%E5%AE%AB%E5%BB%B7'}, {'n': '神话', 'v': '%E7%A5%9E%E8%AF%9D'}, {'n': '商战', 'v': '%E5%95%86%E6%88%98'}, {'n': '警匪', 'v': '%E8%AD%A6%E5%8C%AA'}, {'n': '动作', 'v': '%E5%8A%A8%E4%BD%9C'}, {'n': '惊悚', 'v': '%E6%83%8A%E6%82%9A'}, {'n': '剧情', 'v': '%E5%89%A7%E6%83%85'}, {'n': '同性', 'v': '%E5%90%8C%E6%80%A7'}, {'n': '奇幻', 'v': '%E5%A5%87%E5%B9%BB'}, {'n': '其它', 'v': '%E5%85%B6%E5%AE%83'}]}, {'key': 'area', 'name': '地區', 'values': [{'n': '全部地区', 'v': ''}, {'n': '大陆', 'v': '%E5%A4%A7%E9%99%86'}, {'n': '香港', 'v': '%E9%A6%99%E6%B8%AF'}, {'n': '台 湾', 'v': '%E5%8F%B0%E6%B9%BE'}, {'n': '日本', 'v': '%E6%97%A5%E6%9C%AC'}, {'n': '韩国', 'v': '%E9%9F%A9%E5%9B%BD'}, {'n': '欧美', 'v': '%E6%AC%A7%E7%BE%8E'}, {'n': '泰国', 'v': '%E6%B3%B0%E5%9B%BD'}, {'n': '新马', 'v': '%E6%96%B0%E9%A9%AC'}, {'n': '其它', 'v': '%E5%85%B6%E5%AE%83'}]}, {'key': 'lang', 'name': '語言', 'values': [{'n': '全部语言', 'v': ''}, {'n': '国语', 'v': '%E5%9B%BD%E8%AF%AD'}, {'n': '粤语', 'v': '%E7%B2%A4%E8%AF%AD'}, {'n': '英语', 'v': '%E8%8B%B1%E8%AF%AD'}, {'n': '韩语', 'v': '%E9%9F%A9%E8%AF%AD'}, {'n': '日语', 'v': '%E6%97%A5%E8%AF%AD'}, {'n': '西班牙', 'v': '%E8%A5%BF%E7%8F%AD%E7%89%99'}, {'n': '法语', 'v': '%E6%B3%95%E8%AF%AD'}, {'n': '德语', 'v': '%E5%BE%B7%E8%AF%AD'}, {'n': '泰语', 'v': '%E6%B3%B0%E8%AF%AD'}, {'n': '其它', 'v': '%E5%85%B6%E5%AE%83'}]}, {'key': 'year', 'name': '時 間', 'values': [{'n': '全部时间', 'v': ''}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90%E5%B9%B4%E4%BB%A3'}, {'n': '80年代', 'v': '80%E5%B9%B4%E4%BB%A3'}, {'n': '更早', 'v': '%E6%9B%B4%E6%97%A9'}]}]}
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
		if(filter):
			result['filters'] = self.config['filter']					
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
		url = f'{self.siteUrl}/ajax/data?mid=1&page={pg}&limit=35&tid={tid}'
		'''
		by = extend.get("by") if "by" in extend else "time"
		cls = extend.get("by") if "class" in extend else ""
		area = extend.get("area") if "area" in extend else ""
		lang = extend.get("lang") if "lang" in extend else ""
		year = extend.get("year") if "year" in extend else ""
		result['mid'] = 1
		result['by'] = by
		result['tid'] = tid
		result['page'] = pg
		result['class'] = cls
		result['year'] = year
		result['lang'] = lang
		result['area'] = area
		result['limit'] = 35
		url = self.siteUrl + "/ajax/data"
		'''
		return self.fetch(url,headers=self.header)
	
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