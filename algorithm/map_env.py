import numpy as np
import cv2
from MapApi import MapApi
import time


class Environment:
    def __init__(self, map_size = 100, obs_rate = 0.2):
        self.mapApi = MapApi()
        self.map, self.pos = self.mapApi.getEniv()
        self.lastTime = time.time()
        self.step  = 0
        self.score = self.mapApi.score
        self.posx, self.posy = self.pos
        self.GameOver = False
        self.deltaTime = []

#    def reset(self):
#        self.step = 0
#        self.score = 0
#        self.posx = 0
#        self.posy = 0
#        self.__pkg_score = 10
#        #map definition: 0-free  1-occupy  
#        self.map = np.zeros((self.map_size,self.map_size),'int')
#        obs_cnt = int(self.map_size**2*self.obs_rate)
#        self.map[tuple(np.random.randint(0,self.map_size,obs_cnt)),tuple(np.random.randint(0,self.map_size,obs_cnt))] = -1
#        self.map[0,0] = 0
#        self.__add_package()

#    def load(self, file):
#        data = [int(x) for x in open(file).readline().strip().split(' ')]
#        self.map_size = data[0]
#        self.map = np.reshape(data[1:],(self.map_size,self.map_size))

    # move dir (0,1,2,3) => (up, down, left, right)
    def move(self, movdir):
        r,c = self.map.shape[:2]
        invalid_move = False
        if movdir == 0: # up
            if self.posx>0 and self.map[self.posx-1,self.posy]>=0:
                self.posx -= 1
            else:
                invalid_move = True
        elif movdir == 1: #down
            if self.posx<r-1 and self.map[self.posx+1,self.posy]>=0:
                self.posx += 1
            else:
                invalid_move = True
        elif movdir == 2: # left
            if self.posy>0 and self.map[self.posx,self.posy-1]>=0:
                self.posy -= 1
            else:
                invalid_move = True
        elif movdir == 3: #right
            if self.posy<c-1 and self.map[self.posx,self.posy+1]>=0:
                self.posy += 1
            else:
                invalid_move = True
        if not invalid_move:
            self.step += 1
            self.map, self.pos, self.score, cur_score, self.GameOver= self.mapApi.move(movdir)
            curTime = time.time()
            self.deltaTime.append(curTime-self.lastTime)
            print(self.deltaTime[-1])
            self.lastTime = curTime
            if (self.posx, self.posy) != self.pos:
                self.posx, self.posy = self.pos
                print('error: direction errors')
        self.watch()
#        cur_score = self.map[self.posx,self.posy]
#        if cur_score > 0:
#            self.score += cur_score
#            self.map[self.posx,self.posy] = 0

        #update map scores
#        self.map[self.map>0] -= 1

        #update map packages
#        if np.random.random()>0.3:
#            self.__add_package()

        return invalid_move, self.score
    
    
#    def __add_package(self):
#        r,c = self.map.shape[:2]
#        while True:
#            i = np.random.randint(r)
#            j = np.random.randint(c)
#            if self.map[i,j] == 0:
#                self.map[i,j] = self.__pkg_score
#                break

    def get_show_map(self, K=20):
        r,c = self.map.shape
        drawimg = cv2.cvtColor(np.ones((r*K,c*K),'uint8')+254, cv2.COLOR_GRAY2BGR)
        for i in range(c):
            drawimg = cv2.line(drawimg, (0,i*K), (r*K,i*K), (250,0,0), 1)
        for i in range(r):
            drawimg = cv2.line(drawimg, (i*K,0), (i*K,c*K), (250,0,0), 1)

        for i in range(r):
            for j in range(c):
                if self.map[i,j]>0:
                    drawimg[i*K:i*K+K, j*K:j*K+K] = (0, 170*self.map[i,j]/36+80, 0)
                    drawimg = cv2.putText(drawimg, '%d'%self.map[i,j], (int((j+0.1)*K),int((i+0.8)*K)), cv2.FONT_HERSHEY_SIMPLEX, K*0.02, (255,0,0), 2)
                elif self.map[i,j]<0:
                    drawimg[i*K:i*K+K, j*K:j*K+K] = (50, 50, 50)
        
        drawimg = cv2.circle(drawimg, (int((self.posy+0.5)*K),int((self.posx+0.5)*K)), int(K/3), (0,0,255), -1)
        
        status_bar = np.ones((30,c*K,3),'uint8')+128
        status_bar = cv2.putText(status_bar, 'step:%d score:%d'%(self.step,self.score), (0,17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
        return np.vstack([drawimg,status_bar])

    def watch(self):
        cv2.imshow('map', self.get_show_map())

if __name__ == '__main__':
    for epoch in range(100):
        map_size = 20
        sim = Environment(20)
        while sim.step<=500:
            sim.watch()
            key = cv2.waitKey(100)
            if key == 27:
                exit()
            sim.move(np.random.choice([0,1,2,3]))
