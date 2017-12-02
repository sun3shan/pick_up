# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 20:21:13 2017

@author: SF-A05
"""

import flask
import requests
import webbrowser
import numpy as np
import time
import codecs

import wx
import wx.html2

import os




class Map:
    def __init__(self, data):
        self.MapSize = data['MapSize']
        self.Parcels = data['Parcels']
        self.Courier = data['courier']
        self.Courier['pos'] = (self.Courier['pos']['X'], self.Courier['pos']['Y'])
        self.visibleBarriers = data['visibleBarriers']
        self.Map = np.zeros((self.MapSize, self.MapSize), dtype=int)
        self.Barriers = []
        for bar in self.visibleBarriers:
            bar['pos'] = (bar['pos']['X'], bar['pos']['Y'])
            self.Barriers.append(bar)
            self.Map[bar['pos']] = -1
        for parcel in self.Parcels:
            parcel['pos'] = (parcel['pos']['X'], parcel['pos']['Y'])
            self.Map[parcel['pos']] = parcel['value']
        self.browser = webbrowser.get()
        self.isOpen = False
        self.showMap()
#    
    
    def showMap(self):
        rsp = session.get(url + '/showResult')
        data = rsp.text
        f = codecs.open('static/result.html', 'w', 'utf-8')
        f.write(data)
        f.close()
        self.isOpen = self.browser.open(os.getcwd()+'\\static\\result.html', new=0, autoraise=False) if not self.isOpen else True
        
    def refresh(self, data):
        self.Parcels = data['Parcels']
        self.Courier = data['courier']
        self.Courier['pos'] = (self.Courier['pos']['X'], self.Courier['pos']['Y'])
        self.visibleBarriers = data['visibleBarriers']
        self.Map = np.zeros((self.MapSize, self.MapSize), dtype=int)
        self.Barriers = []
        for bar in self.visibleBarriers:
            bar['pos'] = (bar['pos']['X'], bar['pos']['Y'])
            self.Barriers.append(bar)
            self.Map[bar['pos']] = -1
        for parcel in self.Parcels:
            parcel['pos'] = (parcel['pos']['X'], parcel['pos']['Y'])
            self.Map[parcel['pos']] = parcel['value']
        self.showMap()
        
    def canGo(self, direction):
        nextPos = list(self.Courier['pos'])
        if direction == 0:
            nextPos[1] += 1
        elif direction == 1:
            nextPos[0] -= 1
        elif direction == 2:
            nextPos[0] += 1
        elif direction == 3:
            nextPos[1] -= 1
        if -1 in nextPos or self.MapSize in nextPos or self.Map[tuple(nextPos)]==-1:
            return False
        else:
            return True
        
#        
        
class MyBrowser(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((1000, 1000))

if __name__=='__main__':
#    app = wx.App()
    url = 'http://127.0.0.1:5000'
    go_url = {0:'/down', 1:'/left', 2:'/right', 3:'/up'}
    session = requests.session()
    rsp = session.get(url)
    data = rsp.json()
    myMap = Map(data)
    direction = myMap.Courier['direction']
    for i in range(500):
        while True:
#            if myMap.canGo(direction):
#                break
            if direction == 0:
                if myMap.canGo(1):
                    direction = 1
                elif myMap.canGo(0):
                    direction = 0
                elif myMap.canGo(2):
                    direction = 2
                elif myMap.canGo(3):
                    direction = 3
                break
            elif direction == 1:
                if myMap.canGo(3):
                    direction = 3
                elif myMap.canGo(1):
                    direction = 1
                elif myMap.canGo(0):
                    direction = 0
                elif myMap.canGo(2):
                    direction = 2
                break
            elif direction == 2:
                if myMap.canGo(0):
                    direction = 0
                elif myMap.canGo(2):
                    direction = 2
                elif myMap.canGo(3):
                    direction = 3
                elif myMap.canGo(1):
                    direction = 1
                break
            elif direction == 3:
                if myMap.canGo(2):
                    direction = 2
                elif myMap.canGo(3):
                    direction = 3
                elif myMap.canGo(1):
                    direction = 1
                elif myMap.canGo(0):
                    direction = 0
                break
            if not direction in range(4):
                direction = 0
        rsp = session.get(url+go_url[direction])
        data = rsp.json()
        myMap.refresh(data)
        direction = myMap.Courier['direction']
        
        time.sleep(0.7)
