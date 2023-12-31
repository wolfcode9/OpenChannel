#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import base64
import re
from urllib import request, parse
import urllib
import urllib.request
# import ssl
import json
# ssl._create_default_https_context = ssl._create_unverified_context#全局取消证书验证
class Spider(Spider):  # 元类 默认的元类 type
	def getName():
		return "看剧网"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"内地剧": "neidiju",
			"欧美剧":"oumeiju",
			"日剧":"riju",
			"韩剧":"hanju",
			"港剧":"gangju",
			"台剧":"taiju",
			"泰剧":"taiguoju",
			"其它剧":"haiwaiju",
			"国漫":"guoman",
			"日漫":"riman",
			"美漫":"meiman",
			"最近更新":"new",
			"排行榜":"top"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		htmlTxt=self.custom_webReadFile(urlStr='https://www.kanju5.com/',header=self.header)
		element =self.html(htmlTxt)
		nodes = element.xpath('//ul/li/a')
		videos=[]
		head="https://www.kanju5.com"
		for a in nodes:
			if len(a.xpath('./div[@class="cap"]'))<1 or len(a.xpath('./img'))<1:
				continue
			title=a.xpath('./img/@alt')[0]
			img=a.xpath('./img/@src')[0]
			url=a.xpath("./@href")[0]
			if url.find('://')<1:
				url=head+url
			if img.find('://')<1:
				img=head+img
			vod_id="{0}###{1}###{2}".format(title,url,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		result = {
			'list':videos
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		videos=[]
		Url='https://www.kanju5.com/category/{0}/page/{1}'.format(tid,pg)
		htmlTxt=self.custom_webReadFile(urlStr=Url,header=self.header)
		root = self.html(htmlTxt)
		nodes = root.xpath('//*[@id="content"]/div[@class="post-grid clearfix"]/div[@class="post clearfix"]/div[@class="entry-thumb-left"]/a')
		videos = self.custom_list(aList=nodes)
		pagecount=0 if len(videos)<5 or len(tid)==3 else int(pg)+1
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] =pagecount
		result['limit'] = len(videos)
		result['total'] = 999999
		return result
	def detailContent(self,array):
		aid = array[0].split('###')
		idUrl=aid[1]
		title=aid[0]
		pic=aid[2]
		url=idUrl
		playFrom = []
		htmlTxt =  self.custom_webReadFile(urlStr=url,header=self.header)
		# root=etree.HTML(htmlTxt)
		root = self.html(htmlTxt)
		nodes = root.xpath('//*[@id="content"]/div/div[@class="entry-content lazyload"]/div[@class="play_list_nav"]/a')
		playFrom=[v.text for v in nodes ]
		if len(playFrom)<1:
			return  {'list': []}
		videoList=[]
		vodItems = []
		circuit=root.xpath('//*[@class="play_list"]/ul')
		for v in circuit:
			vodItems=self.custom_EpisodesList(nodes=v)
			vodItems.reverse()
			joinStr = "#".join(vodItems)
			videoList.append(joinStr)
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		
		typeName=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'类型:(.+?)<br',Index=1)
		year=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'<a href="https://www.kanju5.com/tag/([0-9]{4})"',Index=1)
		area=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'制片国家/地区:(.+?)<br',Index=1)
		act=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'主演:(.+?)<br',Index=1)
		dir=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'导演:(.+?)<br',Index=1)
		remarks=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'语言:(.+?)<br',Index=1)
		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name":self.custom_removeHtml(txt=typeName),
			"vod_year": self.custom_removeHtml(txt=year),
			"vod_area": self.custom_removeHtml(txt=area),
			"vod_remarks": self.custom_removeHtml(txt=remarks),
			"vod_actor":  self.custom_removeHtml(txt=act),
			"vod_director": self.custom_removeHtml(txt=dir),
			"vod_content": ''
		}
		vod['vod_play_from'] = vod_play_from
		vod['vod_play_url'] = vod_play_url

		result = {
			'list': [
				vod
			]
		}
		return result

	def searchContent(self,key,quick):
		url="https://www.kanju5.com/?s="+urllib.parse.quote(key)
		htmlTxt=self.custom_webReadFile(urlStr=url,header=self.header)
		# root=etree.HTML(htmlTxt)
		root = self.html(htmlTxt)
		nodes = root.xpath('//*[@class="entry-thumb lazyload"]')
		videos=self.custom_list(aList=nodes)
		result = {
			'list':videos
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		Url=id
		parse=1
		htmlTxt =self.custom_webReadFile(urlStr=Url,header=self.header)
		fc=self.custom_RegexGetText(Text=htmlTxt,RegexText=r'fc:\s*\t*"(.+?)",',Index=1)		
		if fc!='':
			headers = {
				"Referer": id,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
				"Host":'www.kanju5.com'
			}
			data="height=500&fc="+urllib.parse.quote(fc)
			req = request.Request(url='https://www.kanju5.com/player/player.php', data=bytes(data, encoding='utf8'),headers=headers, method='POST')
			response = request.urlopen(req)
			htmlTxt=response.read().decode('utf-8')
			try:
				jo =json.loads(htmlTxt)
				link =self.custom_RegexGetText(Text=jo['show'].strip(),RegexText=r'src=\s*\t*".+?url=(.+?)"',Index=1)
				if link!='':
					Url=str(base64.b64decode(link),encoding='utf8')
					parse=0
			except :
				pass
		result["parse"] = parse#0=直接播放、1=嗅探
		result["playUrl"] =''
		result["url"] = Url
		# result['jx'] = jx#VIP解析,0=不解析、1=解析
		result["header"] = ''	
		return result


	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'https://www.kanju5.com',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
		"Host":'www.kanju5.com'
		}
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
	#-----------------------------------------------自定义函数-----------------------------------------------
		#正则取文本
	def custom_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	#分类取结果
	def custom_list(self,aList):
		videos = []
		head="https://www.kanju5.com"
		for a in aList:
			title=a.xpath('./@title')[0]
			img=a.xpath('./img/@src')[0]
			url=a.xpath("./@href")[0]
			if url.find('://')<1:
				url=head+url
			if img.find('://')<1:
				img=head+img
			vod_id="{0}###{1}###{2}".format(title,url,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		return videos
		#访问网页
	def custom_webReadFile(self,urlStr,header=None,codeName='utf-8'):
		html=''
		if header==None:
			header={
				"Referer":urlStr,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
				"Host":self.custom_RegexGetText(Text=urlStr,RegexText='https*://(.*?)(/|$)',Index=1)
			}
		req=urllib.request.Request(url=urlStr,headers=header)#,headers=header
		with  urllib.request.urlopen(req)  as response:
			html = response.read().decode(codeName)
		return html
	#取集数
	def custom_EpisodesList(self,nodes):
		videos = []
		head="https://www.kanju5.com"
		ListLi=nodes.xpath('./li/a')
		for vod in ListLi:
			title =vod.xpath("./text()")[0]
			url = vod.xpath("./@href")[0]
			# print(title)
			if len(url) == 0:
				continue
			videos.append(title+"$"+head+url)
		return videos
	#删除html标签
	def custom_removeHtml(self,txt):
		soup = re.compile(r'<[^>]+>',re.S)
		txt =soup.sub('', txt)
		return txt.replace("&nbsp;"," ")
	
# T=Spider()
# l=T.searchContent(key='柯南',quick='')
# # l=T.homeVideoContent()
# # # extend={'types':'netflix',"area":"韩国","year":"2023","lang":"韩语","sort":"score"}
# l=T.categoryContent(tid='neidiju',pg='1',filter=False,extend={})
# print(len(l['list']))
# for x in l['list']:
# 	print(x['vod_id'])
# mubiao='黑白密码 (2023)###https://www.kanju5.com/views/cwodlky.html###https://img.kanju5.com/2023/11/16/U2N2Q5Z.jpg'#l['list'][0]['vod_id']#7
# # # print(mubiao)
# playTabulation=T.detailContent(array=[mubiao,])
# print(playTabulation)
# vod_play_from=playTabulation['list'][0]['vod_play_from']
# vod_play_url=playTabulation['list'][0]['vod_play_url']
# url=vod_play_url.split('$$$')
# vod_play_from=vod_play_from.split('$$$')[0]
# url=url[0].split('$')
# url=url[1].split('#')[0]
# # print(url)
# m3u8=T.playerContent(flag=vod_play_from,id=url,vipFlags=True)
# print(m3u8['url'])