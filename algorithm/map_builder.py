import numpy as np
import cv2
import os

def on_mouse(event,x,y,flags,param):
    param.mouse_cb(event,x,y,flags)

class MapCreator:
    def __init__(self, map_size = 100, obs_rate = 0.2):
        self.map_size = map_size
        self.obs_rate = obs_rate
        self.reset()
        self.K = 20
        self.left_mouse_down = False
        self.right_mouse_down = False

    def reset(self):
        self.map = np.zeros((self.map_size,self.map_size),'int')
        obs_cnt = int(self.map_size**2*self.obs_rate)
        self.map[tuple(np.random.randint(0,self.map_size,obs_cnt)),tuple(np.random.randint(0,self.map_size,obs_cnt))] = -1
        self.map[0,0] = 0

    def load(self, file):
        data = [int(x) for x in open(file).readline().strip().split(' ')]
        self.map_size = data[0]
        self.map = np.reshape(data[1:],(self.map_size,self.map_size))

    def save(self, file):
        open(file,'w').write(' '.join([str(x) for x in [self.map_size]+self.map.ravel().tolist()]))

    def mouse_cb(self,event,x,y,flags):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.left_mouse_down = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.left_mouse_down = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.right_mouse_down = True
        elif event == cv2.EVENT_RBUTTONUP:
            self.right_mouse_down = False

        r = int(y/self.K)
        c = int(x/self.K)
        if r<0 or c<0 or r>=self.map.shape[0] or c>=self.map.shape[1]:
            return
        if self.left_mouse_down:
            self.map[r,c] = -1
        elif self.right_mouse_down:
            self.map[r,c] = 0

    def watch(self, winname='map'):
        cv2.namedWindow(winname)
        cv2.setMouseCallback(winname, on_mouse, self)
        K = self.K
        while True:
            r,c = self.map.shape[:2]
            drawimg = cv2.cvtColor(np.ones((r*K,c*K),'uint8')+254, cv2.COLOR_GRAY2BGR)
            for i in range(c):
                drawimg = cv2.line(drawimg, (0,i*K), (r*K,i*K), (250,0,0), 1)
            for i in range(r):
                drawimg = cv2.line(drawimg, (i*K,0), (i*K,c*K), (250,0,0), 1)

            for i in range(r):
                for j in range(c):
                    if self.map[i,j]<0:
                        drawimg[i*K:i*K+K, j*K:j*K+K] = (50, 50, 50)

            cv2.imshow(winname, drawimg)
            key = cv2.waitKey(100)
            if key == 27 or key == ord('s') or key == 32 or key == 13 or key == 10:
                return key
            elif key == ord('r'):
                self.reset()
            elif key == ord('c'):
                self.map[:] = 0


def create_maps():
    save_path = 'maps'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    mc = MapCreator(15)
    for i in range(0,200):
        save_file = os.path.join(save_path,'%03d.map'%i)
        if os.path.exists(save_file):
            mc.load(save_file)
            print('%s exists, load it'%save_file)
        key = mc.watch()
        if key==ord('s'):
            mc.save(save_file)
            print('save map %s'%save_file)
            mc.reset()
        elif key==27:
            break

def modify_map(map_file):
    if not os.path.exists(map_file):
        print('no files, %s'%map_file)
        return
    mc = MapCreator(15)
    mc.load(map_file)
    key = mc.watch()
    if key==ord('s'):
        mc.save(map_file)
        print('save map %s'%map_file)

if __name__ == '__main__':
    # create_maps()
    modify_map('maps/1.map')
