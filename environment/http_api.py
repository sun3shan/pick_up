# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 00:07:35 2017

@author: kuang shan
"""

from flask import Flask, render_template, session, json, jsonify
import random as rnd
import os

rnd.seed(100)

app = Flask(__name__,static_url_path='',root_path='D:/Code/SF/pick_up/environment')

@app.route('/', methods=['GET','POST'])
def index():
    data = {}
    courier = {'pos':{'X':0, 'Y':0}, 'direction':0, 'step': 0, 'score':0}
    Barriers = genBarriers(courier['pos'])
    Parcels = genParcels(Barriers=Barriers, courierPos=courier['pos'])
    session['courier'] = courier
    session['Barriers'] = Barriers
    session['Parcels'] = Parcels
    data['courier'] = str(courier).replace('\'','')
    data['Barriers'] = str(Barriers).replace('\'','')
    data['Parcels'] = str(Parcels).replace('\'','')
    return json.dumps(data)#render_template('main.html', data = data)
    
def genBarriers(courierPos):
    barNums =  rnd.randint(5, 15)
    Barriers = []
    Sets = [(i,j) for i in range(10) for j in range(10) if i!=courierPos['X'] and j!=courierPos['Y']]
    for i in range(barNums):
        barrier = rnd.choice(Sets)
        Sets.remove(barrier)
        Barriers.append({'pos':{'X':barrier[0], 'Y':barrier[1]}})
    return Barriers

def genParcels(Barriers, courierPos, Parcels = []):
    parcelNums = rnd.randint(5, 15)
    Sets = [(i,j) for i in range(10) for j in range(10) if i!=courierPos['X'] and j!=courierPos['Y']]
    for barrier in Barriers:
        Sets.remove((barrier['pos']['X'], barrier['pos']['Y']))
    for i in range(parcelNums):
        parcel = rnd.choice(Sets)
        Sets.remove(parcel)
        Parcels.append({'pos':{'X': parcel[0], 'Y': parcel[1]}, 'value':10})
    return Parcels

def canGo(pos):
    Barriers = session['Barriers']
    if pos['X']<0 or pos['X']>9 or pos['Y']<0 or pos['Y']>9:
        return False
    for barriers in Barriers:
        if pos == barriers['pos']:
            return False
    return True

def getScore(pos):
    Parcels = session['Parcels']
    score = 0
    for parcel in Parcels:
        if pos == parcel['pos']:
            score = parcel['value']
            Parcels.remove(parcel)
        parcel['value'] -= 1
        if parcel['value'] == 0:
            Parcels.remove(parcel)
    session['Parcels'] = Parcels
    return score

@app.route('/left')
def goLeft():
    courier = session['courier']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 1
    if canGo({'X':courier['pos']['X']-1, 'Y':courier['pos']['Y']}):
        courier['pos']['X'] -= 1
    
    courier['score'] += getScore(courier['pos'])
    session['courier'] = courier
    data = {'courier':courier, 'Parcels':session['Parcels'], 'Barriers':session['Barriers']}
    return json.dumps(data)


@app.route('/right')
def goRight():
    courier = session['courier']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 2
    if canGo({'X':courier['pos']['X']+1, 'Y':courier['pos']['Y']}):
        courier['pos']['X'] += 1
    
    courier['score'] += getScore(courier['pos'])
    session['courier'] = courier
    data = {'courier':courier, 'Parcels':session['Parcels'], 'Barriers':session['Barriers']}
    return json.dumps(data)


@app.route('/up')
def goUp():
    courier = session['courier']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 3
    if canGo({'X':courier['pos']['X'], 'Y':courier['pos']['Y']-1}):
        courier['pos']['Y'] -= 1
    
    courier['score'] += getScore(courier['pos'])
    session['courier'] = courier
    data = {'courier':courier, 'Parcels':session['Parcels'], 'Barriers':session['Barriers']}
    return json.dumps(data)


@app.route('/down')
def goDown():
    courier = session['courier']
    if courier['step'] == 500:
        return 'Game Over'
    courier['step'] += 1
    courier['direction'] = 0
    if canGo({'X':courier['pos']['X'], 'Y':courier['pos']['Y']+1}):
        courier['pos']['Y'] += 1
    
    courier['score'] += getScore(courier['pos'])
    session['courier'] = courier
    data = {'courier':courier, 'Parcels':session['Parcels'], 'Barriers':session['Barriers']}
    return json.dumps(data)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()