# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 08:30:21 2017

@author: SF-A05
"""

import requests
import numpy as np

URL = 'http://10.2.5.64/test'
Direction = ['U', 'D', 'L', 'R']
class MapApi():
    def __init__(self):
        self.team = 'KOPB'
        self.env_id = ''
        self.score = 0
    
    def getEniv(self):
        while True:
            rsp = requests.post(URL, data={'name': self.team})
            data = rsp.json()
            if(data['msg']=='OK'):
                self.env_id = data['id']
                self.map, self.cur_pos = self.decodeState(data['state'])
                print(data['id'])
                return self.map, self.cur_pos
    
    def move(self, direction):
        while True:
            rsp = requests.post(URL + '/'+ self.env_id + '/move', json={'direction': Direction[direction]})
            data = rsp.json()
            if data['msg']=='OK':
                self.env_id = data['id']
                self.map, self.cur_pos = self.decodeState(data['state'])
                self.score += data['reward']
                return self.map, self.cur_pos, self.score, data['reward'], data['done']
            else:
                return 'error'
            
    def decodeState(self, state):
        _map = np.zeros((12, 12))
        for wall in state['walls']:
            _map[wall['x'], wall['y']] = -1
        for job in state['jobs']:
            _map[job['x'], job['y']] = job['value']
        cur_pos = (state['ai']['x'],state['ai']['y'])
        return _map, cur_pos
        
    
if __name__ == '__main__':
#    rsp = requests.post(URL, data={'name': ''})
#    data = rsp.json()
#    print(data)
#    print(URL + '/'+ data['id'] + '/move')
#    rsp = requests.post(URL + '/'+ data['id'] + '/move', json={'direction': Direction[1]})
#    data = rsp.json()
#    print(data)
    mapApi = MapApi()
    print(mapApi.getEniv())
    print(mapApi.move(1))
    print(mapApi.move(3))
    print(mapApi.move(0))
    print(mapApi.move(2))    