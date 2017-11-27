# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 23:46:46 2017

@author: kss
"""

def assess(cur_map, packages, currentPos=(0, 0), residualStep=10, Path=[]):
    for pack in packages:
        path = pathplan_astar(cur_map, currentPos, pack['pos'], pack['value'])
        path_len = len(path)
        if path_len<pack['value']:
            if residualStep==10:
                Path.append([{'getPackages':[], 'getScore':0}])
            Path[-1]['getPackages'].append(pack)
            Path[-1]['getScore'] += pack['value']-path_len
            if residualStep-path_len > 0:
                otherPackages = [{'No':p['No'], 'pos':p['pos'], 'value':p['value']-path_len} for p in packages if p!=pack and p['value']-path_len>0]
                if len(otherPackages)>0:
                    assess(cur_map, otherPackages, pack['pos'], residualStep-path_len, Path)
    return Path
            
            
    