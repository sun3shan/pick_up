# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 00:07:35 2017

@author: kuang shan
"""

from flask import Flask, render_template, session, json, jsonify
import random as rnd
import os
import webbrowser
import time

rnd.seed(100)

mapSize = 30
visibleRange = 2
refreshTime = 2
maxParcelNum = 10

app = Flask(__name__,static_url_path='',root_path=os.getcwd())

def getVisibleBarriers(Barriers, curPos, visibleRange):
    visibleBarriers = []
    for bar in Barriers:
        if abs(bar['pos']['X']-curPos['X'])<=visibleRange and abs(bar['pos']['Y']-curPos['Y'])<=visibleRange:
            visibleBarriers.append(bar)
    return visibleBarriers
    
def genBarriers(courierPos):
    barNums =  rnd.randint(15, 30)
    Barriers = []
    Sets = [(i,j) for i in range(mapSize) for j in range(mapSize) if i!=courierPos['X'] and j!=courierPos['Y']]
    for i in range(barNums):
        barrier = rnd.choice(Sets)
        Sets.remove(barrier)
        Barriers.append({'pos':{'X':barrier[0], 'Y':barrier[1]}})
    return Barriers

def genParcels(Barriers, courierPos, Parcels = []):
    parcelNums = rnd.randint(3, 8)
    Sets = [(i,j) for i in range(mapSize) for j in range(mapSize) if i!=courierPos['X'] and j!=courierPos['Y']]
    for barrier in Barriers:
        if (barrier['pos']['X'], barrier['pos']['Y']) in Sets:
            Sets.remove((barrier['pos']['X'], barrier['pos']['Y']))
    for parcel in Parcels:
        if (parcel['pos']['X'], parcel['pos']['Y']) in Sets:
            Sets.remove((parcel['pos']['X'], parcel['pos']['Y']))
    for i in range(parcelNums):
        parcel = rnd.choice(Sets)
        Sets.remove(parcel)
        Parcels.append({'pos':{'X': parcel[0], 'Y': parcel[1]}, 'value':10})
    return Parcels

def canGo(pos):
    Barriers = session['Barriers']
    if pos['X']<0 or pos['X']>=mapSize or pos['Y']<0 or pos['Y']>=mapSize:
        return False
    for barriers in Barriers:
        if pos == barriers['pos']:
            return False
    return True

def getScore(pos, step):
    Parcels = session['Parcels']
    newParcels = []
    score = 0
    for parcel in Parcels:
        if pos == parcel['pos']:
            score = parcel['value']
            parcel['value'] = 0
        else:
            parcel['value'] -=  1 if step%(mapSize/10)==0 else 0
        if parcel['value'] > 0:
            newParcels.append(parcel)
    session['Parcels'] = newParcels
    return score

def rndGenParcels():
    curTime = int(time.time())
    lastTime = int(session['lastTime'])
    Parcels = session['Parcels']
#    startTime = int(session['startTime'])
    if (lastTime!=curTime and (curTime-lastTime)>refreshTime or rnd.randint(1, 6)%2==0) and len(Parcels)<maxParcelNum:
        Barriers = session['Barriers']
        courier = session['courier']
        Parcels = genParcels(Barriers, courier['pos'], Parcels)
        session['Parcels'] = Parcels
    session['lastTime'] = curTime
        
    


@app.route('/', methods=['GET','POST'])
def index():
    data = {}
    courier = {'pos':{'X':0, 'Y':0}, 'direction':0, 'step': 0, 'score':0}
    Barriers = genBarriers(courier['pos'])
    visibleBarriers = getVisibleBarriers(Barriers, courier['pos'], visibleRange)
    Parcels = genParcels(Barriers=Barriers, courierPos=courier['pos'], Parcels=[])
    print(len(Barriers), len(visibleBarriers))
    session['courier'] = courier
    session['Barriers'] = Barriers
    session['visibleBarriers'] = visibleBarriers
    session['Parcels'] = Parcels
    session['startTime'] = int(time.time())
    session['lastTime'] = session['startTime']
    data['courier'] = courier
    data['Parcels'] = Parcels
    data['visibleBarriers'] = visibleBarriers
    data['MapSize'] = mapSize
    return json.dumps(data)#render_template('main.html', data = data)

@app.route('/showResult', methods=['GET', 'POST'])
def showResult():
    data = {}
    data['courier'] = str(session['courier']).replace('\'', '')
#    data['Barriers'] = str(session['visibleBarriers']).replace('\'', '')
    data['Barriers'] = str(session['Barriers']).replace('\'', '')
    data['Parcels'] = str(session['Parcels']).replace('\'', '')
    data['MapSize'] = mapSize
    return render_template('main.html', data = data)

@app.route('/left')
def goLeft():
    courier = session['courier']
    Barriers = session['Barriers']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 1
    if canGo({'X':courier['pos']['X']-1, 'Y':courier['pos']['Y']}):
        courier['pos']['X'] -= 1
    
    courier['score'] += getScore(courier['pos'], courier['step'])
    session['courier'] = courier
    visibleBarriers = getVisibleBarriers(Barriers, courier['pos'], visibleRange)
    session['visibleBarriers'] = visibleBarriers
    rndGenParcels()
    data = {'courier':courier, 'Parcels':session['Parcels'], 'visibleBarriers':visibleBarriers, 'mapSize':mapSize}
    return json.dumps(data)


@app.route('/right')
def goRight():
    courier = session['courier']
    Barriers = session['Barriers']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 2
    if canGo({'X':courier['pos']['X']+1, 'Y':courier['pos']['Y']}):
        courier['pos']['X'] += 1
    
    courier['score'] += getScore(courier['pos'], courier['step'])
    session['courier'] = courier
    visibleBarriers = getVisibleBarriers(Barriers, courier['pos'], visibleRange)
    session['visibleBarriers'] = visibleBarriers
    rndGenParcels()
    data = {'courier':courier, 'Parcels':session['Parcels'], 'visibleBarriers':visibleBarriers, 'mapSize':mapSize}
    return json.dumps(data)


@app.route('/up')
def goUp():
    courier = session['courier']
    Barriers = session['Barriers']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 3
    if canGo({'X':courier['pos']['X'], 'Y':courier['pos']['Y']-1}):
        courier['pos']['Y'] -= 1
    
    courier['score'] += getScore(courier['pos'], courier['step'])
    session['courier'] = courier
    visibleBarriers = getVisibleBarriers(Barriers, courier['pos'], visibleRange)
    session['visibleBarriers'] = visibleBarriers
    rndGenParcels()
    data = {'courier':courier, 'Parcels':session['Parcels'], 'visibleBarriers':visibleBarriers, 'mapSize':mapSize}
    return json.dumps(data)


@app.route('/down')
def goDown():
    courier = session['courier']
    Barriers = session['Barriers']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 0
    if canGo({'X':courier['pos']['X'], 'Y':courier['pos']['Y']+1}):
        courier['pos']['Y'] += 1
    
    courier['score'] += getScore(courier['pos'], courier['step'])
    session['courier'] = courier
    visibleBarriers = getVisibleBarriers(Barriers, courier['pos'], visibleRange)
    session['visibleBarriers'] = visibleBarriers
    rndGenParcels()
    data = {'courier':courier, 'Parcels':session['Parcels'], 'visibleBarriers':visibleBarriers, 'mapSize':mapSize}
    return json.dumps(data)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()