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
    Q = sp.homeContent(True) # 主页
    #Q = sp.homeVideoContent() # 主页视频
    #Q = sp.detailContent(["2200"]) # 详情
    #Q = sp.categoryContent('dsj','1',False,{}) # 分类
    #Q = sp.searchContent("dota",False) # 搜索    
    #Q = sp.playerContent("","bXZfMjIwMC1ubV8x",{}) # 播放
    print(Q)
                        
if __name__ == '__main__':
    pyname = "py_app.py"
    extend = "https://kuaikan-api.com/api.php/provide/vod/from/kuaikan"
    run(pyname,extend=extend)
    