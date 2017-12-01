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

def strategy_greedy(env):
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score

    # run your strategy
    targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
    max_value = -1
    best_dir = -1
    for tx,ty in targets:
        tar_score = cur_map[tx,ty]
        if abs(tx-cx)+abs(ty-cy)>tar_score:
            continue
        path = pathplan_astar(cur_map, (cx,cy), (tx,ty), tar_score)
        path_len = len(path)
        if path_len==0:
            continue
        tar_value = tar_score-path_len
        # tar_value /= path_len
        # print('tar (%d,%d) path:%d tar_value:%d'%(tx,ty,path_len,tar_value))
        if path_len>0 and tar_value>0 and tar_value>max_value:
            max_value = tar_value
            best_dir = path2dir((cx,cy),path[0])
    return best_dir if best_dir>=0 else np.random.choice([0,1,2,3])

def strategy_greedy2(env):
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score

    # run your strategy
    targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
    targets = [(tx,ty) for tx,ty in targets if abs(tx-cx)+abs(ty-cy)<cur_map[tx,ty]]

    max_value = -1
    best_dir = -1
    for tx,ty in targets:
        tar_score = cur_map[tx,ty]
        path = pathplan_astar(cur_map, (cx,cy), (tx,ty), tar_score)
        path_len = len(path)
        if path_len==0 or path_len>tar_score:
            continue
        heading_list = [(tx,ty)]
        tar_value = tar_score-path_len
        # tar_value /= path_len
        # print('tar (%d,%d) path:%d tar_value:%d'%(tx,ty,path_len,tar_value))
        if tar_value>max_value:
            max_value = tar_value
            best_dir = path2dir((cx,cy),path[0])

        for tx2,ty2 in targets:
            if (tx2,ty2) in heading_list:
                continue
            tar2_score = cur_map[tx2,ty2]
            path2 = pathplan_astar(cur_map, (tx,ty), (tx2,ty2), tar2_score-path_len)
            path2_len = len(path2)
            if path2_len==0 or path_len+path2_len>tar2_score:
                continue
            heading_list2 = heading_list+[(tx2,ty2)]
            tar_value2 = tar_score - path_len + tar2_score - path2_len
            if tar_value2>max_value:
                max_value = tar_value2
                best_dir = path2dir((cx,cy),path[0])

    return best_dir if best_dir>=0 else np.random.choice([0,1,2,3])

def strategy_greedy2(env):
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score

    # run your strategy
    targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
    targets = [(tx,ty) for tx,ty in targets if abs(tx-cx)+abs(ty-cy)<cur_map[tx,ty]]

    max_value = -1
    best_dir = -1
    for tx,ty in targets:
        tar_score = cur_map[tx,ty]
        path = pathplan_astar(cur_map, (cx,cy), (tx,ty), tar_score)
        path_len = len(path)
        if path_len==0 or path_len>tar_score:
            continue
        heading_list = [(tx,ty)]
        tar_value = tar_score-path_len
        # tar_value /= path_len
        # print('tar (%d,%d) path:%d tar_value:%d'%(tx,ty,path_len,tar_value))
        if tar_value>max_value:
            max_value = tar_value
            best_dir = path2dir((cx,cy),path[0])

        for tx2,ty2 in targets:
            if (tx2,ty2) in heading_list:
                continue
            tar2_score = cur_map[tx2,ty2]
            path2 = pathplan_astar(cur_map, (tx,ty), (tx2,ty2), tar2_score-path_len)
            path2_len = len(path2)
            if path2_len==0 or path_len+path2_len>tar2_score:
                continue
            heading_list2 = heading_list+[(tx2,ty2)]
            tar_value2 = tar_score - path_len + tar2_score - path2_len
            if tar_value2>max_value:
                max_value = tar_value2
                best_dir = path2dir((cx,cy),path[0])

    return best_dir if best_dir>=0 else np.random.choice([0,1,2,3])


def greedy_recursion(targets, cur_map, cur_pos, tar_list, cur_dir, cur_len, cur_value, max_value, best_dir):
    # print(cur_pos, len(targets), max_value, best_dir)

    for idx,t in enumerate(targets):
        tar_score = cur_map[t[0],t[1]]
        path = pathplan_astar(cur_map, cur_pos, t, tar_score-cur_len)
        path_len = len(path)
        if path_len==0 or path_len+cur_len>tar_score:
            continue
        tdir = path2dir(cur_pos,path[0]) if cur_dir == -1 else cur_dir
        path_value = cur_value + tar_score - path_len - cur_len
        if path_value > max_value+1:
            max_value = path_value
            best_dir = tdir
            # print(tar_list+[t], path_value, tdir)
        max_value2,best_dir2 = greedy_recursion(targets[:idx]+targets[idx+1:], cur_map, t, tar_list+[t], tdir,
            cur_len+path_len, path_value, max_value, best_dir)
        if max_value2 > max_value+1:
            max_value = max_value2
            best_dir = best_dir2
    return max_value, best_dir

#class Node:
#    def __init__(self, curNode):
#        self.curNode = curNode
#        self.childNodes = []
#        self.isLeaf = True
#    def addChild(Node):
#        self.childNodes.append(Node)
#
#
#def genTree(map_cur):
#    
#
#def getDirectionWithNoPath(cur_map):
#    tree = genTree(map_cur)

def packagesSort(cur_map, cur_pos, targets):
    packages = []
    steps = np.ones((12,12))*100
    for tar in targets:
        steps[tar] = len(GLOBAL_PLANER.pathplan(cur_pos, tar))
    while True:
        minStep = steps.min()
        if minStep!=100:
            Pos = (np.reshape(np.where(steps==minStep), (2,-1)).T).tolist()
            for pos in Pos:
                if cur_map[tuple(pos)]-steps[tuple(pos)]>0:
                    packages.append({'pos':tuple(pos), 'value': cur_map[tuple(pos)]})
                steps[pos] = 100
        else:
            break
    
    return packages
def testAssess(env):
    global bestPath, old_map
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score
    cur_pos = (cx, cy)
    
    if not (old_map== cur_map).all() or len(bestPath)==0:
        # run your strategy
        targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
    #    targets = [(tx,ty) for tx,ty in targets if abs(tx-cx)+abs(ty-cy)<cur_map[tx,ty]]
    
        packages = packagesSort(cur_map, cur_pos, targets)
#        for tar in targets:
#            if cur_map[tar]-len(GLOBAL_PLANER.pathplan(cur_pos, tar))>0:
#                packages.append({'pos':tar, 'value':cur_map[tar[0], tar[1]]})
        Path = assess(cur_map, packages, cur_pos, residualStep=min(maxSteps-cur_step, cur_map.max()), Path=[{'path':[],'getPackages':[], 'getScore':0, 'Steps':0, 'Cost':0}])
        if len(Path[-1]['path'])==0:
            Path.pop(-1)
        cost = [path['getScore'] for path in Path if path['getScore']!=0 and path['Steps']!=0]        #*(path['Steps']/(501-cur_step))
    #    cost = [path['Cost'] for path in Path]
        best_dir = -1
        if len(cost)>0:
            maxCost = max(cost)
            indx = cost.index(maxCost)
            if len(Path[indx]['path'])>0:
                bestPath = deepcopy(Path[indx]['path'])
                best_dir = path2dir(cur_pos,Path[indx]['path'][0])
                bestPath.pop(0)
            elif len(packages)>0:
                print('1')
                print(cur_step)
                path = GLOBAL_PLANER.pathplan(cur_pos,packages[0]['pos'])
    #            path = pathplan_astar(cur_map, cur_pos, packages[0]['pos'], 1000)
                if len(path)>0:
                    best_dir = path2dir(cur_pos, path[0])
                    bestPath = deepcopy(path)
                    bestPath.pop(0)
            
        else:
            print('0')
            print(cur_step)
            if len(packages)>0:
                path = GLOBAL_PLANER.pathplan(cur_pos,packages[0]['pos'])
                #path = pathplan_astar(cur_map, cur_pos, packages[0]['pos'], 1000)
                if len(path)>0:
                    best_dir = path2dir(cur_pos, path[0])
                    bestPath = deepcopy(path)
                    bestPath.pop(0)
        del Path
    else:
        best_dir = path2dir(cur_pos, bestPath[0])
        bestPath.pop(0)
    old_map = deepcopy(cur_map)
    
    return best_dir if best_dir in range(4) else np.random.choice([0,1,2,3])

def assess(cur_map, packages, currentPos=(0, 0), residualStep=10, Path=[{'path':[],'getPackages':[], 'getScore':0, 'Steps':0, 'Cost':0}], level = 0):
    curPath = deepcopy(Path[-1])
    for pack in packages:
        path = GLOBAL_PLANER.pathplan(currentPos,pack['pos'])
        #path = pathplan_astar(cur_map, currentPos, pack['pos'], pack['value'])
        path_len = len(path)
        otherPackages = [{'pos':p['pos'], 'value':p['value']-path_len} for p in packages if p!=pack and p['value']-path_len>0]
        isContinue = False
        for other in otherPackages:
            if len(GLOBAL_PLANER.pathplan(currentPos, other['pos']))+len(GLOBAL_PLANER.pathplan(other['pos'], pack['pos'])) <= path_len:
#            if other['pos'] in path:
                isContinue = True
                break
        if isContinue:
            continue
        if path_len<min(residualStep, pack['value']) and path_len>0:
            if curPath!=Path[-1]:
                Path.append(deepcopy(curPath))
            Path[-1]['path'].extend(path)
            Path[-1]['getPackages'].append(pack)
            Path[-1]['getScore'] += pack['value']-path_len
            Path[-1]['Steps'] += path_len
            Path[-1]['Cost'] *= Path[-1]['Steps']/Path[-1]['getScore']
            if residualStep-path_len > 0:
                
                if len(otherPackages)>0:
                    assess(cur_map, otherPackages, pack['pos'], residualStep-path_len, Path, level+1)
                    del otherPackages,path
    if len(curPath['path'])>0 and curPath!=Path[-1]:
        Path.append(deepcopy(curPath))
        
    del curPath, packages
    return Path
            
           

def strategy_greedy3(env):
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score

    # run your strategy
    targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
    targets = [(tx,ty) for tx,ty in targets if abs(tx-cx)+abs(ty-cy)<cur_map[tx,ty]]

    # print('='*25)
    max_value, best_dir = greedy_recursion(targets, cur_map, (cx,cy), [], -1, 0, 0, -1, -1)
    return best_dir if best_dir>=0 else np.random.choice([0,1,2,3])

class MapPlayer:
    def __init__(self, env, strategy_foo, max_step=288):
        self.env = env
        self.strategy_foo = strategy_foo
        self.max_step = 288
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
#        self.Env.append(deepcopy(self.env))
#        self.env = Environment()
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
            self.scores.append(self.play_episode())
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
    # strategy = strategy_random_walk
    # strategy = strategy_greedy
    # strategy = strategy_greedy2
    # strategy = strategy_greedy3
    maxSteps = 288
    strategy = testAssess

    play = MapPlayer(Environment(), strategy)

    ########### watch single round ##############
    #play.play_episode(True, 100)
    play.play_existmap('maps/000.map',True, 100)

    ########### test multi round ################
    play.play_rounds(10, True)



    ########### test exist maps ################
    
#    mapdir = 'maps'
#    scores = []
#    for f in sorted([os.path.join(mapdir,x) for x in os.listdir(mapdir)]):
#        print(f,end='\r')
#        s = play.play_existmap(f)
#        scores.append(s)
#    mean_score = np.mean(scores)
#    max_score = np.max(scores)
#    min_score = np.min(scores)
#    var_score = np.var(scores)
#    open('scores.txt','w').write(' '.join([str(x) for x in scores]))
#    print('Play %d rounds, Average score:%.3f (min:%.3f max:%.3f), var:%.3f'%(len(scores), mean_score,
#        float(min_score),float(max_score),var_score))
    