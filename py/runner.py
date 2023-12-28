#coding=utf-8
#!/usr/bin/python
from importlib.machinery import SourceFileLoader
import os
import sys

def loadFromDisk(fileName):
    name = fileName.split('/')[-1].split('.')[0]
    sp = SourceFileLoader(name, fileName).load_module().Spider()
    return sp

def run(py_name):
    sp = loadFromDisk(py_name)
    sp.init([])

    os.system('cls')
    print()
    print("### 《 推薦 》 ###")
    vod = sp.homeVideoContent()
    if vod:        
        print("》" + str(vod['list'][0]))
        print()

    print("###《 主頁 》###")
    vod = sp.homeContent(False)    
    print("》" + str(vod))
    print()
    if  vod['class']:        
        type_id = vod['class'][0]['type_id']
        
        print("###《 分类 》 ###")
        vod = sp.categoryContent(type_id,'1',False,{})        
        if vod['list']:                     
            vod_id = vod['list'][0]['vod_id']
            vod_name = vod['list'][0]['vod_name']            
            print(vod['list'][0])
            print()

            print("### 《 詳情 》 ###")
            vod = sp.detailContent([vod_id])
            if vod['list']:
                vod_play_url = vod['list'][0]['vod_play_url'].split('$')[1].split('#')[0]                
                print("》" + str(vod['list'][0]))
                print()
                
                if vod_play_url:
                    print("### 《 播放 》 ###")                
                    vod = sp.playerContent("",vod_play_url,{})
                    if vod:                            
                        print("》" + str(vod))
                        print()

            if vod_name:
                print("### 《 搜索 》 ###") 
                vod = sp.searchContent(vod_name,False)                              
                if vod['list']:
                    print("》" + str(vod['list'][0]))                
                    
if __name__ == '__main__':
    argv = sys.argv
    if argv[1]:
        run(argv[1])
    