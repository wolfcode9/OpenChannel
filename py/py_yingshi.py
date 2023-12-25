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
		"filter": {{"1": [{"key": "by", "name": "排序", "values": [{"n": "新上线", "v": "desc"}, {"n": "热播榜", "v": "desc"}, {"n": "好评榜", "v": "desc"}]}, {"key": "class", "name": "類型", "values": [{"n": "全部类型", "v": ""}, {"n": "偶像", "v": "desc"}, {"n": "爱情", "v": "desc"}, {"n": "古装", "v": "desc"}, {"n": "谍战", "v": "desc"}, {"n": "战争", "v": "desc"}, {"n": "江湖", "v": "desc"}, {"n": "武侠", "v": "desc"}, {"n": "言情", "v": "desc"}, {"n": "历史", "v": "desc"}, {"n": "玄幻", "v": "desc"}, {"n": "历险", "v": "desc"}, {"n": "都市", "v": "desc"}, {"n": "科幻", "v": "desc"}, {"n": "军旅", "v": "desc"}, {"n": "喜剧", "v": "desc"}, {"n": "罪案", "v": "desc"}, {"n": "青春", "v": "desc"}, {"n": "家庭", "v": "desc"}, {"n": "悬疑", "v": "desc"}, {"n": "穿越", "v": "desc"}, {"n": "宫廷", "v": "desc"}, {"n": "神话", "v": "desc"}, {"n": "商战", "v": "desc"}, {"n": "警匪", "v": "desc"}, {"n": "动作", "v": "desc"}, {"n": "惊悚", "v": "desc"}, {"n": "剧情", "v": "desc"}, {"n": "同性", "v": "desc"}, {"n": "奇幻", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "area", "name": "地區", "values": [{"n": "全部地区", "v": ""}, {"n": "大陆", "v": "desc"}, {"n": "香港", "v": "desc"}, {"n": "台湾", "v": "desc"}, {"n": "日本", "v": "desc"}, {"n": "韩国", "v": "desc"}, {"n": "欧美", "v": "desc"}, {"n": "泰国", "v": "desc"}, {"n": "新马", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "lang", "name": "語言", "values": [{"n": "全部语言", "v": ""}, {"n": "国语", "v": "desc"}, {"n": "粤语", "v": "desc"}, {"n": "英语", "v": "desc"}, {"n": "韩语", "v": "desc"}, {"n": "日语", "v": "desc"}, {"n": "西班牙", "v": "desc"}, {"n": "法语", "v": "desc"}, {"n": "德语", "v": "desc"}, {"n": "泰语", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "year", "name": "時間", "values": [{"n": "全部时间", "v": ""}, {"n": "2023", "v": "2023"}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014-2011", "v": "2014-2011"}, {"n": "2010-2000", "v": "2010-2000"}, {"n": "90年代", "v": "90%E5%B9%B4%E4%BB%A3"}, {"n": "80年代", "v": "80%E5%B9%B4%E4%BB%A3"}, {"n": "更早", "v": "%E6%9B%B4%E6%97%A9"}]}]}, {"2": [{"key": "by", "name": "排序", "values": [{"n": "新上线", "v": "desc"}, {"n": "热播榜", "v": "desc"}, {"n": "好评榜", "v": "desc"}]}, {"key": "class", "name": "類型", "values": [{"n": "全部类型", "v": ""}, {"n": "喜剧", "v": "desc"}, {"n": "冒险", "v": "desc"}, {"n": "爱情", "v": "desc"}, {"n": "动画电影", "v": "desc"}, {"n": "战争", "v": "desc"}, {"n": "剧情", "v": "desc"}, {"n": "动作", "v": "desc"}, {"n": "恐怖", "v": "desc"}, {"n": "悬疑", "v": "desc"}, {"n": "奇幻", "v": "desc"}, {"n": "灾难", "v": "desc"}, {"n": "同性", "v": "desc"}, {"n": "惊悚", "v": "desc"}, {"n": "歌舞", "v": "desc"}, {"n": "犯罪", "v": "desc"}, {"n": "科幻", "v": "desc"}, {"n": "经典", "v": "desc"}, {"n": "网络电影", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "area", "name": "地區", "values": [{"n": "全部地区", "v": ""}, {"n": "大陆", "v": "desc"}, {"n": "香港", "v": "desc"}, {"n": "台湾", "v": "desc"}, {"n": "日本", "v": "desc"}, {"n": "韩国", "v": "desc"}, {"n": "欧美", "v": "desc"}, {"n": "泰国", "v": "desc"}, {"n": "新马", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "lang", "name": "語言", "values": [{"n": "全部语言", "v": ""}, {"n": "国语", "v": "desc"}, {"n": "粤语", "v": "desc"}, {"n": "英语", "v": "desc"}, {"n": "韩语", "v": "desc"}, {"n": "日语", "v": "desc"}, {"n": "西班牙", "v": "desc"}, {"n": "法语", "v": "desc"}, {"n": "德语", "v": "desc"}, {"n": "泰语", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "year", "name": "時間", "values": [{"n": "全部时间", "v": ""}, {"n": "2023", "v": "2023"}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014-2011", "v": "2014-2011"}, {"n": "2010-2000", "v": "2010-2000"}, {"n": "90年代", "v": "90%E5%B9%B4%E4%BB%A3"}, {"n": "80年代", "v": "80%E5%B9%B4%E4%BB%A3"}, {"n": "更早", "v": "%E6%9B%B4%E6%97%A9"}]}]}, {"3": [{"key": "by", "name": "排序", "values": [{"n": "新上线", "v": "desc"}, {"n": "热播榜", "v": "desc"}, {"n": "好评榜", "v": "desc"}]}, {"key": "class", "name": "類型", "values": [{"n": "全部类型", "v": ""}, {"n": "真人秀", "v": "desc"}, {"n": "选秀", "v": "desc"}, {"n": "网综", "v": "desc"}, {"n": "脱口秀", "v": "desc"}, {"n": "情感", "v": "desc"}, {"n": "搞笑", "v": "desc"}, {"n": "竞技", "v": "desc"}, {"n": "访谈", "v": "desc"}, {"n": "演唱会", "v": "desc"}, {"n": "晚会", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "area", "name": "地區", "values": [{"n": "全部地区", "v": ""}, {"n": "大陆", "v": "desc"}, {"n": "香港", "v": "desc"}, {"n": "台湾", "v": "desc"}, {"n": "日本", "v": "desc"}, {"n": "韩国", "v": "desc"}, {"n": "欧美", "v": "desc"}, {"n": "泰国", "v": "desc"}, {"n": "新马", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "lang", "name": "語言", "values": [{"n": "全部语言", "v": ""}, {"n": "国语", "v": "desc"}, {"n": "粤语", "v": "desc"}, {"n": "英语", "v": "desc"}, {"n": "韩语", "v": "desc"}, {"n": "日语", "v": "desc"}, {"n": "西班牙", "v": "desc"}, {"n": "法语", "v": "desc"}, {"n": "德语", "v": "desc"}, {"n": "泰语", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "year", "name": "時間", "values": [{"n": "全部时间", "v": ""}, {"n": "2023", "v": "2023"}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014-2011", "v": "2014-2011"}, {"n": "2010-2000", "v": "2010-2000"}, {"n": "90年代", "v": "90%E5%B9%B4%E4%BB%A3"}, {"n": "80年代", "v": "80%E5%B9%B4%E4%BB%A3"}, {"n": "更早", "v": "%E6%9B%B4%E6%97%A9"}]}]}, {"4": [{"key": "by", "name": "排序", "values": [{"n": "新上线", "v": "desc"}, {"n": "热播榜", "v": "desc"}, {"n": "好评榜", "v": "desc"}]}, {"key": "class", "name": "類型", "values": [{"n": "全部类型", "v": ""}, {"n": "热血", "v": "desc"}, {"n": "格斗", "v": "desc"}, {"n": "少女", "v": "desc"}, {"n": "科幻", "v": "desc"}, {"n": "推理", "v": "desc"}, {"n": "灵异", "v": "desc"}, {"n": "机战", "v": "desc"}, {"n": "竞技", "v": "desc"}, {"n": "魔幻", "v": "desc"}, {"n": "爆笑", "v": "desc"}, {"n": "冒险", "v": "desc"}, {"n": "恋爱", "v": "desc"}, {"n": "校园", "v": "desc"}, {"n": "治愈", "v": "desc"}, {"n": "泡面", "v": "desc"}, {"n": "穿越", "v": "desc"}, {"n": "耽美", "v": "desc"}, {"n": "动画电影", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "area", "name": "地區", "values": [{"n": "全部地区", "v": ""}, {"n": "大陆", "v": "desc"}, {"n": "香港", "v": "desc"}, {"n": "台湾", "v": "desc"}, {"n": "日本", "v": "desc"}, {"n": "韩国", "v": "desc"}, {"n": "欧美", "v": "desc"}, {"n": "泰国", "v": "desc"}, {"n": "新马", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "lang", "name": "語言", "values": [{"n": "全部语言", "v": ""}, {"n": "国语", "v": "desc"}, {"n": "粤语", "v": "desc"}, {"n": "英语", "v": "desc"}, {"n": "韩语", "v": "desc"}, {"n": "日语", "v": "desc"}, {"n": "西班牙", "v": "desc"}, {"n": "法语", "v": "desc"}, {"n": "德语", "v": "desc"}, {"n": "泰语", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "year", "name": "時間", "values": [{"n": "全部时间", "v": ""}, {"n": "2023", "v": "2023"}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014-2011", "v": "2014-2011"}, {"n": "2010-2000", "v": "2010-2000"}, {"n": "90年代", "v": "90%E5%B9%B4%E4%BB%A3"}, {"n": "80年代", "v": "80%E5%B9%B4%E4%BB%A3"}, {"n": "更早", "v": "%E6%9B%B4%E6%97%A9"}]}]}, {"5": [{"key": "by", "name": "排序", "values": [{"n": "新上线", "v": "desc"}, {"n": "热播榜", "v": "desc"}, {"n": "好评榜", "v": "desc"}]}, {"key": "class", "name": "類型", "values": [{"n": "全部类型", "v": ""}, {"n": "文化", "v": "desc"}, {"n": "探索", "v": "desc"}, {"n": "军事", "v": "desc"}, {"n": "解密", "v": "desc"}, {"n": "科技", "v": "desc"}, {"n": "历史", "v": "desc"}, {"n": "人物", "v": "desc"}, {"n": "自然", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "area", "name": "地區", "values": [{"n": "全部地区", "v": ""}, {"n": "大陆", "v": "desc"}, {"n": "香港", "v": "desc"}, {"n": "台湾", "v": "desc"}, {"n": "日本", "v": "desc"}, {"n": "韩国", "v": "desc"}, {"n": "欧美", "v": "desc"}, {"n": "泰国", "v": "desc"}, {"n": "新马", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "lang", "name": "語言", "values": [{"n": "全部语言", "v": ""}, {"n": "国语", "v": "desc"}, {"n": "粤语", "v": "desc"}, {"n": "英语", "v": "desc"}, {"n": "韩语", "v": "desc"}, {"n": "日语", "v": "desc"}, {"n": "西班牙", "v": "desc"}, {"n": "法语", "v": "desc"}, {"n": "德语", "v": "desc"}, {"n": "泰语", "v": "desc"}, {"n": "其它", "v": "desc"}]}, {"key": "year", "name": "時間", "values": [{"n": "全部时间", "v": ""}, {"n": "2023", "v": "2023"}, {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"}, {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"}, {"n": "2014-2011", "v": "2014-2011"}, {"n": "2010-2000", "v": "2010-2000"}, {"n": "90年代", "v": "90%E5%B9%B4%E4%BB%A3"}, {"n": "80年代", "v": "80%E5%B9%B4%E4%BB%A3"}, {"n": "更早", "v": "%E6%9B%B4%E6%97%A9"}]}]}}
	}

	def getName(self):
		return "影視"
	
	def init(self,extend=""):
		pass	
	
	#主頁
	def homeContent(self,filter):
		result = {}		
		classes = []
		filter = []
		cateManual = {
			"電視劇": "1",
			"電影": "2",
			"綜藝": "3",
			"動漫": "4",
			"記錄片": "5"
		}	
		
		for k in cateManual:
			classes.append({'type_name': k,'type_id': cateManual[k]})
			fi = self.job(cateManual[k])
			filter.append({cateManual[k]: fi})
		
		result['class'] = classes
		g = ', '.join(json.dumps(item, ensure_ascii=False) for item in filter)
		result['filters'] = g
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