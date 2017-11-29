from __future__ import print_function
import pdb
import numpy as np
import cv2
import os
from map_env import Environment
from pathplan import pathplan_astar
from copy import deepcopy

import time

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


def testAssess(env):
    # information you can get. NOTE:do not change these values
    cx = env.posx
    cy = env.posy
    cur_map = env.map
    cur_step = env.step
    cur_score = env.score
    cur_pos = (cx, cy)

    # run your strategy
    targets = [(tx,ty) for tx,ty in np.reshape(np.where(cur_map>0),(2,-1)).T]
#    targets = [(tx,ty) for tx,ty in targets if abs(tx-cx)+abs(ty-cy)<cur_map[tx,ty]]

    packages = []
    for tar in targets:
        packages.append({'pos':tar, 'value':cur_map[tar[0], tar[1]]})
    Path = assess(cur_map, packages, cur_pos, residualStep=(500-cur_step if cur_step>490 else 10), Path=[{'path':[],'getPackages':[], 'getScore':0, 'Steps':0, 'Cost':0}])
    if len(Path[-1]['path'])==0:
        Path.pop(-1)
    Steps = [path['Steps'] for path in Path if path['Steps']>10]
    if len(Steps)>0:
        print(Path)
        time.sleep(6)
    cost = [path['Steps']/path['getScore'] for path in Path if path['getScore']!=0 and path['Steps']!=0]        #*(path['Steps']/(501-cur_step))
#    cost = [path['Cost'] for path in Path]
    best_dir = -1
    if len(cost)>0:
        maxCost = min(cost)
        indx = cost.index(maxCost)
        if len(Path[indx]['path'])>0:
            best_dir = path2dir(cur_pos,Path[indx]['path'][0])
        elif len(packages)>0:
            path = pathplan_astar(cur_map, cur_pos, packages[0]['pos'], 1000)
            if len(path)>0:
                best_dir = path2dir(cur_pos, path[0])
    else:
        if len(packages)>0:
            path = pathplan_astar(cur_map, cur_pos, packages[0]['pos'], 1000)
            if len(path)>0:
                best_dir = path2dir(cur_pos, path[0])

    
    return best_dir if best_dir in range(4) else np.random.choice([0,1,2,3])

def assess(cur_map, packages, currentPos=(0, 0), residualStep=10, Path=[{'path':[],'getPackages':[], 'getScore':0, 'Steps':0, 'Cost':0}], level = 0):
    curPath = deepcopy(Path[-1])
#    print('Packages')
#    print(packages)
#    print('residual      '+str(residualStep))
#    print('')
#    print('lastPath')
#    print(Path[-1])
#    print('')
    for pack in packages:
#        print('level                 '+str(level))
#        print('residual      '+str(residualStep))
        path = pathplan_astar(cur_map, currentPos, pack['pos'], pack['value'])
        path_len = len(path)
        if path_len<min(residualStep, pack['value']) and path_len>0:
#            print('curPath')
#            print(curPath)
#            print('')
#            print('lastPath')
#            print(Path[-1])
#            print('')
#            print('residual      '+str(residualStep))
            if curPath!=Path[-1]:
                Path.append(deepcopy(curPath))
#            print('lastPath')
#            print(Path[-1])
#            print('')
            Path[-1]['path'].extend(path)
            Path[-1]['getPackages'].append(pack)
            Path[-1]['getScore'] += pack['value']-path_len
            Path[-1]['Steps'] += path_len
#            print('Path')
#            print(Path[-1])
#            print('')
#            print('curPath')
#            print(curPath)
#            print('')
#            print(curPath==Path[-1])
            if Path[-1]['Steps']>10:
                print('Path')
                print(Path[-1])
                print('')
                print('path')
                print(path)
                print('')
                print('residual      '+str(residualStep))
                print('package')
                print(pack)
                time.sleep(10)
            Path[-1]['Cost'] *= Path[-1]['Steps']/Path[-1]['getScore']
            if residualStep-path_len > 0:
                otherPackages = [{'pos':p['pos'], 'value':p['value']-path_len} for p in packages if p!=pack and p['value']-path_len>0]
                if len(otherPackages)>0:
#                    print('otherPackages')
#                    print(otherPackages)
#                    print('')
#                    print('path_len           ' + str(path_len))
                    assess(cur_map, otherPackages, pack['pos'], residualStep-path_len, Path, level+1)
                    del otherPackages,path
    if len(curPath['path'])>0 and curPath!=Path[-1]:
        Path.append(deepcopy(curPath))
        
    del curPath, packages
#    if len(Path)>1:
#        print('lastPath')
#        print(Path[-1])
#        print('')
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
    def __init__(self, env, strategy_foo, max_step=500):
        self.env = env
        self.strategy_foo = strategy_foo
        self.max_step = 500

    def play_episode(self, show_step = False, wait_ms = 100):
        self.env.reset()
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
        self.env.reset()
        self.env.load(mapfile)
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
        scores = []
        for i in range(round_cnt):
            scores.append(self.play_episode())
            if verbose:
                print('%d/%d'%(i+1,round_cnt),end='\r')
        print('%d/%d'%(i+1,round_cnt))

        scores = np.array(scores)
        mean_score = np.mean(scores)
        if verbose:
            max_score = np.max(scores)
            min_score = np.min(scores)
            var_score = np.var(scores)
            print('Play %d rounds, Average score:%.3f (min:%.3f max:%.3f), var:%.3f'%(round_cnt, mean_score,
                float(min_score),float(max_score),var_score))
            print(scores)

        return mean_score

if __name__ == '__main__':
    ########### select strategy  ################
    # strategy = strategy_random_walk
    # strategy = strategy_greedy
    # strategy = strategy_greedy2
    # strategy = strategy_greedy3
    strategy = testAssess

    play = MapPlayer(Environment(10), strategy)

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
    