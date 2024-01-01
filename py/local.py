#coding=utf-8
#!/usr/bin/python
from importlib.machinery import SourceFileLoader
import os

def loadFromDisk(fileName):
    name = fileName.split('/')[-1].split('.')[0]
    sp = SourceFileLoader(name, fileName).load_module().Spider()
    return sp

def run(pyname,extend):
    sp = loadFromDisk(pyname)  #载入本地脚本
    sp.init(extend) # 初始化
    #Q = sp.homeContent(True) # 主页
    #Q = sp.homeVideoContent() # 主页视频
    #Q = sp.detailContent(["2200"]) # 详情
    #Q = sp.categoryContent('dsj','1',False,{}) # 分类
    Q = sp.searchContent("陌上人如",False) # 搜索 
    #Q = sp.playerContent("","bXZfMjIwMC1ubV8x",{}) # 播放
    print(Q['list'][0])
                        
if __name__ == '__main__':
    pyname = "py_app.py"
    extend = "https://kuaikan-api.com/api.php/provide/vod/from/kuaikan"
    run(pyname,extend=extend)


#飛速V	https://www.feisuzyapi.com/api.php/provide/vod/
#速播V	https://subocaiji.com/api.php/provide/vod/at/json
#量子V	https://cj.lziapi.com/api.php/provide/vod/
#快看	https://kuaikan-api.com/api.php/provide/vod/from/kuaikan
#非凡V	https://cj.ffzyapi.com/api.php/provide/vod/
#暴風	https://bfzyapi.com/api.php/provide/vod
# ?ac=videolist&search?text=dota&pg=1
# ?ac=videolist&zm=dota&page=1
# ?ac=videolist&wd=dota&page=1
# /list?wd=dota&page=1
# ?wd=dota&page=1