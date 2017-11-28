# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 20:21:13 2017

@author: SF-A05
"""

import flask
import requests
import numpy as np

class Map:
    def __init__(self, data):
        self.MapSize = data['mapSize']
        self.Parcels = data['Parcels']
        self.Courier = data['Courier']
        self.visibleBarriers = data['visibleBarriers']
        self.Map = np.zeros((self.MapSize, self.MapSize), dtype=int)
        self.Barriers = []
        for bar in self.visibleBarriers:
            self.Barriers.append(bar)
            self.Map[bar['pos']] = -1
        for parcel in self.Parcels:
            self.Map[parcel['pos']] = parcel['value']
    
    def show()

if __name__=='__main__':
    session = requests.session()
    rsp = session.get('http://127.0.0.1:5000')
    data = rsp.json()