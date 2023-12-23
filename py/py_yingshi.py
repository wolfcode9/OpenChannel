# coding=utf-8
# !/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import base64
from Crypto.Cipher import AES
import json
import requests
import concurrent.futures
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup

class Spider(Spider):
    def __init__(self):
        self.site_url = "https://www.yingshi.tv"
        self.service = concurrent.futures.ThreadPoolExecutor()

    def get_cache(self):
        return FileUtil.get_cache_file("ying_shi_home")

    def get_headers(self):
        headers = {
            "User-Agent": Utils.CHROME,
            "Referer": self.site_url
        }
        return headers

    def init(self, context, extend):
        self.service = concurrent.futures.ThreadPoolExecutor()

    def home_content(self, filter):
        if self.get_cache().exists():
            return FileUtil.read(self.get_cache())

        classes = [
            Class("1", "電視劇"),
            Class("2", "電影"),
            Class("4", "動漫"),
            Class("3", "綜藝"),
            Class("5", "紀錄片")
        ]

        filters = {}
        for class_type in classes:
            filters[class_type.get_type_id()] = self.service.submit(self.job, class_type.get_type_id()).result()

        result = Result.string(classes, filters)
        FileUtil.write(self.get_cache(), result)
        return result

    def home_video_content(self):
        response = requests.get(self.site_url)
        doc = BeautifulSoup(response.text, "html.parser")
        video_list = []
        for e in doc.select("div#desktop-container").select("li.ys_show_item"):
            id = e.select("a").attr("href").split("/")[4]
            pic = e.select("img").attr("src")
            name = e.select("h2.ys_show_title").text()
            remark = e.select("span.ys_show_episode_text").text()
            if name:
                video_list.append(Vod(id, name, pic, remark))
        return Result.string(video_list)

    def category_content(self, tid, pg, filter, extend):
        by = extend.get("by", "time")
        cls = extend.get("class", "")
        area = extend.get("area", "")
        lang = extend.get("lang", "")
        year = extend.get("year", "")

        params = {
            "mid": "1",
            "by": by,
            "tid": tid,
            "page": pg,
            "class": cls,
            "year": year,
            "lang": lang,
            "area": area,
            "limit": "35"
        }

        url = f"{self.site_url}/ajax/data"
        return requests.get(url, params=params, headers=self.get_headers()).text

    def detail_content(self, ids):
        url = f"{self.site_url}/vod/play/id/{ids[0]}/sid/1/nid/1.html"
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        json_data = re.search('let data = (.*);', doc.text).group(1)
        json_data = json_data.replace("&amp;", " ")
        vod = Vod.object_from(json_data)
        return Result.string(vod)

    def player_content(self, flag, id, vip_flags):
        proxy_url = f"{Proxy.get_url()}?do=yingshi&url={id}"
        return Result.get().url(id).m3u8().string()

    def search_content(self, key, quick, pg="1"):
        params = {
            "mid": "1",
            "page": pg,
            "limit": "18",
            "wd": key
        }
        url = f"{self.site_url}/ajax/search.html"
        return requests.get(url, params=params, headers=self.get_headers()).text

    def job(self, type_id):
        url = f"https://www.yingshi.tv/vod/show/by/hits_day/id/{type_id}/order/desc.html"
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        filters = [
            self.filter(doc.select("div.ys_filter_list_show_types").select("div.ys_filter.flex")[1].select("div > div"), "by", "排序", 4),
            self.filter(doc.select("div#ys_filter_by_class").select("div > div"), "class", "類型", 6),
            self.filter(doc.select("div#ys_filter_by_country").select("div > div"), "area", "地區", 4),
            self.filter(doc.select("div#ys_filter_by_lang").select("div > div"), "lang", "語言", 8),
            self.filter(doc.select("div#ys_filter_by_year").select("div > div"), "year", "時間", 10)
        ]
        return filters

    def filter(self, elements, key, name, index):
        values = []
        for e in elements:
            n = e.select("p").text
            all_value = "全部" in n
            v = "" if all_value else e.select("a").attr("href").split("/")[index].replace(".html", "")
            values.append(Filter.Value(n, v))
        return Filter(key, name, values)

    @staticmethod
    def vod(params):
        url = params.get("url")
        ad_block = ["10.0099", "8.1748"]  # Advertisement ts
        content = requests.get(url).text
        m = re.finditer("#EXT-X-DISCONTINUITY[\\s\\S]*?(?=#EXT-X-DISCONTINUITY|$)", content)
        for match in m:
            k = 0
            digit = re.finditer("#EXTINF:(\\d+\\.\\d+)", match.group(0))
            for d in digit:
                g = float(d.group(1))
                k += g
            for ads in ad_block:
                if ads in str(k):
                    content = content.replace(match.group(0), "")
                    print("Found ads:", ads)
        return 200, "application/octet-stream", content
    
class FileUtil:
    @staticmethod
    def get_cache_file(file_name):
        # 實現 get_cache_file 方法的邏輯
        pass

    @staticmethod
    def read(file):
        # 實現 read 方法的邏輯
        pass

    @staticmethod
    def write(file, content):
        # 實現 write 方法的邏輯
        pass


class Utils:
    CHROME = "Chrome"  # 請確保在 Utils 類中定義 CHROME


class Class:
    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def get_type_id(self):
        return self.type_id


class Filter:
    class Value:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    def __init__(self, key, name, values):
        self.key = key
        self.name = name
        self.values = values


class Result:
    @staticmethod
    def string(data):
        # 實現 string 方法的邏輯
        pass

    @staticmethod
    def get():
        # 實現 get 方法的邏輯
        pass


class Proxy:
    @staticmethod
    def get_url():
        # 實現 get_url 方法的邏輯
        pass


class Vod:
    def __init__(self, id, name, pic, remark):
        self.id = id
        self.name = name
        self.pic = pic
        self.remark = remark

    @staticmethod
    def object_from(json_data):
        # 實現 object_from 方法的邏輯
        pass