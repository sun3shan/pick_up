from __future__ import print_function
import pdb
import numpy as np
import cv2
import os
from map_env import Environment
from pathplan import pathplan_astar
from copy import deepcopy

import time
from dijkstra_offline import GridmapDijkstraOffline

GLOBAL_PLANER = GridmapDijkstraOffline()
old_map = np.zeros((12,12))
bestPath = []
canGetPackages = []


def strategy_random_walk(env):
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score

    # run your strategy

    # make your decision
    movedir = np.random.choice([0,1,2,3])
    return movedir

def path2dir(cur_pos, next_pos):
    dx = next_pos[0] - cur_pos[0]
    dy = next_pos[1] - cur_pos[1]
    if dx==-1 and dy==0:
        return 0
    elif dx==1 and dy==0:
        return 1
    elif dx==0 and dy==-1:
        return 2
    elif dx==0 and dy==1:
        return 3
    else:
        return -1


p = []
ta = []
s = None
def packagesSort(cur_map, cur_pos, targets):
    global p, ta
    packages = []
    steps = np.ones((12,12), dtype=int)*np.Inf
    for tar in targets:
        if cur_map[tar]-len(GLOBAL_PLANER.pathplan(cur_pos, tar))>0:
            steps[tar] = len(GLOBAL_PLANER.pathplan(cur_pos, tar))
    while True:
        minStep = steps.min()
        if minStep!=np.Inf:
            Pos = (np.reshape(np.where(steps==minStep), (2,-1)).T).tolist()
            for pos in Pos:
                packages.append({'pos':tuple(pos), 'value': cur_map[tuple(pos)]})
                steps[tuple(pos)] = np.Inf
        else:
            break
    return packages

# 评估函数
def testAssess(env):
    global bestPath, old_map, canGetPackages
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score
    cur_pos = (cx, cy)
    lastTime = int(time.time())
    
    # 如果地图发生更新
    if not (old_map== cur_map).all() or len(bestPath)==0:
        # run your strategy
        targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
        
        
        # 获取地图上可获得的包裹
        packages = packagesSort(cur_map, cur_pos, targets)
        
        # 获取n层递归下的所有路径
        Path = assess(env, cur_map, packages, cur_pos, residualStep=min(maxSteps-cur_step, cur_map.max()), Path=[{'path':[],'getPackages':[], 'getScore':0, 'Steps':0, 'Cost':0}])
        if len(Path[-1]['path'])==0:
            Path.pop(-1)
        
        # 评估函数
        cost = [path['getScore']/path['Steps'] for path in Path if path['getScore']!=0 and path['Steps']!=0] 

        best_dir = -1
        if len(cost)>0:
            # 评估函数最大的路径
            maxCost = max(cost)
            indx = cost.index(maxCost)
            if len(Path[indx]['path'])>0:
                bestPath = deepcopy(Path[indx]['path'])
                canGetPackages = deepcopy(Path[indx]['getPackages'])
                best_dir = path2dir(cur_pos,Path[indx]['path'][0])
        else:
            print('0')
            print(cur_step)
            if len(packages)>0:
                path = GLOBAL_PLANER.pathplan(cur_pos,packages[0]['pos'])
                if len(path)>0:
                    best_dir = path2dir(cur_pos, path[0])
                    bestPath = deepcopy(path)
                    canGetPackages = [deepcopy(packages[0])]
        old_map = deepcopy(cur_map)
        del Path
    # 如果地图没有发生更新
    else:
        best_dir = path2dir(cur_pos, bestPath[0])
        
    if len(bestPath)>0:
        if bestPath[0]==canGetPackages[0]['pos']:
            old_map[bestPath[0]] = 0
            canGetPackages.pop(0)
        else:
            old_map = deepcopy(cur_map)
        bestPath.pop(0)
    for tar in np.reshape(np.where(old_map==1),(2,-1)).T:
        old_map[tuple(tar)] = 0
    if cur_step%40==0:
        print(str(int(time.time())-lastTime)+'           '+str(cur_step) + '        ' + str(cur_score) + '           '+ str(best_dir))
    return best_dir if best_dir in range(4) else np.random.choice([0,1,2,3])

def assess(env, cur_map, packages, currentPos=(0, 0), residualStep=10, Path=[{'path':[],'getPackages':[], 'getScore':0, 'Steps':0, 'Cost':0}], level = 0):

    curPath = deepcopy(Path[-1])
    for pack in packages[0:int(len(packages))]:
        path = GLOBAL_PLANER.pathplan(currentPos,pack['pos'])
        path_len = len(path)
        
        isContinue = False
        otherPackages = []
        for p in packages:
            if p!=pack and p['value']-path_len>0:
                other = {'pos':p['pos'], 'value':p['value']-path_len}
                otherPackages.append(other)
                if len(GLOBAL_PLANER.pathplan(currentPos, other['pos']))+len(GLOBAL_PLANER.pathplan(other['pos'], pack['pos'])) <= path_len:

                    isContinue = True
                    break
        if isContinue:
            del otherPackages,path
            continue
        if path_len<min(residualStep, pack['value']) and path_len>0:
            if curPath!=Path[-1]:
                Path.append(deepcopy(curPath))
            Path[-1]['path'].extend(path)
            Path[-1]['getPackages'].append(pack)
            Path[-1]['getScore'] += pack['value']-path_len
            Path[-1]['Steps'] += path_len
            if len(otherPackages)>0 and level<5:
                assess(env, cur_map, otherPackages, pack['pos'], residualStep-path_len, Path, level+1)
            del otherPackages,path
    if len(curPath['path'])>0 and curPath!=Path[-1]:
        Path.append(deepcopy(curPath))
        
    del curPath, packages
    return Path
            
  

class MapPlayer:
    def __init__(self, env, strategy_foo, max_step=288):
        self.env = env
        self.strategy_foo = strategy_foo
        self.max_step = 400
        self.Env = []

    def play_episode(self, show_step = False, wait_ms = 100):
        self.Env.append(deepcopy(self.env))
        self.env = Environment()
        for i in range(self.max_step):
            movedir = self.strategy_foo(self.env)
            self.env.move(movedir)
            if show_step:
                self.env.watch()
                key = cv2.waitKey(wait_ms)
                if key==27:
                    break
        return self.env.score

    def play_existmap(self, mapfile, show_step = False, wait_ms = 100):
        for i in range(self.max_step):
            movedir = self.strategy_foo(self.env)
            self.env.move(movedir)
            if show_step:
                self.env.watch()
                key = cv2.waitKey(wait_ms)
                if key==27:
                    break
        return self.env.score

    def play_rounds(self, round_cnt, verbose = False):
        self.scores = []
        for i in range(round_cnt):
            startTime = int(time.time())
            self.scores.append(self.play_episode())
            print('score:    ' + str(self.scores[-1]))
            print('time:     ' + str(int(time.time())-startTime))
            if verbose:
                print('%d/%d'%(i+1,round_cnt),end='\r')
        print('%d/%d'%(i+1,round_cnt))

        self.scores = np.array(self.scores)
        mean_score = np.mean(self.scores)
        if verbose:
            max_score = np.max(self.scores)
            min_score = np.min(self.scores)
            var_score = np.var(self.scores)
            print('Play %d rounds, Average score:%.3f (min:%.3f max:%.3f), var:%.3f'%(round_cnt, mean_score,
                float(min_score),float(max_score),var_score))
            print(self.scores)

        return mean_score

if __name__ == '__main__':
    ########### select strategy  ################
    maxSteps = 400
    strategy = testAssess
    env = Environment()
    play = MapPlayer(env, strategy)


    ########### test multi round ################
    play.play_rounds(10, True)


    