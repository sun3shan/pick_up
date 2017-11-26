# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 00:07:35 2017

@author: kuang shan
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    initPos = {'X':0, 'Y':0}
    Barriers = [{'pos':{'X':3, 'Y':5}}, {'pos':{'X':3, 'Y':7}}, {'pos':{'X':6, 'Y':4}}, {'pos':{'X':8, 'Y':3}}]
    Parcels = [{'pos':{'X':5, 'Y':3}, 'value':10}, {'pos':{'X':5, 'Y':3}, 'value':10}, {'pos':{'X':3, 'Y':8}, 'value':10}, {'pos':{'X':5, 'Y':7}, 'value':10}]
    return render_template('main.html', initPos = initPos, Barriers=Barriers, Parcels=Parcels)

if __name__ == '__main__':
    app.run()