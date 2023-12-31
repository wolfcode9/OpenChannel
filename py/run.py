#coding=utf-8
#!/usr/bin/python
from importlib.machinery import SourceFileLoader
import os
import sys

def loadFromDisk(fileName):
    name = fileName.split('/')[-1].split('.')[0]
    sp = SourceFileLoader(name, fileName).load_module().Spider()
    return sp


sp = loadFromDisk("py_app.py")
sp.init([])
vod = sp.searchContent("大指挥家","")
print(vod)