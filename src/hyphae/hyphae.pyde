
from functools import reduce
from hyphae import Hyphae

XMAX, YMAX = 680, 680

def gradient_ring(x,y,r1,r2,rgb1,rgb2,mod=0.5):
    noFill()
    strokeWeight(2)
    for i in range(r1, r2):
        lc = lerpColor(rgb1, rgb2, (float(i)-r1) / (r2-r1))
        
        print "lc:", lc
        stroke(lc)
        circle(x,y,i)

def in_square(bounds, x, y):
    x1,y1,x2,y2 = bounds
    return not (x > x2 or x < x1 or y > y2 or y < y1)

def in_circle(bounds, x, y):
    x1,y1,r = bounds
    
    return sqrt((x-x1)**2 + (y-y1)**2) <= r

def tri_points(x,y,h):
    return [
        (x , y - (h/2)),
        (x - (h/2), y + (h/2)),
        (x + (h/2), y+ (h/2))
    ]

class LineHyphae(Hyphae):
    def __init__(self, seed_points, bounds, f_bounds):
        Hyphae.__init__(self, seed_points, bounds, f_bounds)

    def draw_bounds(self):
        if len(self.bounds) == 3:
            x,y,r = self.bounds 
            r *= 2
            
            gradient_ring(int(x*XMAX), 
                          int(y*YMAX), 
                          int(r*XMAX), 
                          int(r*XMAX)+50, 
                          color(255,255,255), 
                          color(0,0,0))
    
    def draw_branch(self, x1, y1, r1, x2, y2, r2, the):
        stroke(255)
            
        strokeWeight((self.WEIGHT * r2) + 1)
        line(int(x1 * XMAX), int(y1 * YMAX), int(x2 * XMAX), int(y2 * YMAX))
    
    def draw_circle(self, x, y, rad, rgb):
        fill(*rgb)
        circle(int(x * XMAX), int(y * YMAX), rad * 450.)
    

Hys = []
def setup():
    size(XMAX, YMAX)
    
    
    frameRate(800)
    background(0)
    smooth()
 
    global Hys
    
    Hys.append(LineHyphae(seed_points=tri_points(0.25,0.25,0.1),
                          bounds=(0.25, 0.25, 0.2), 
                          f_bounds=in_circle))
    Hys.append(LineHyphae(seed_points=tri_points(0.75,0.25,0.1),
                          bounds=(0.75, 0.25, 0.2), 
                          f_bounds=in_circle))
    Hys.append(LineHyphae(seed_points=tri_points(0.50,0.75,0.1),
                          bounds=(0.50, 0.75, 0.2), 
                          f_bounds=in_circle))
    
    stroke(255)
    
    for Hy in Hys:
        Hy.draw_bounds()
    
    global x
    x = mouseX
    
def draw():
    if keyPressed:
        if key == 's':
            saveFrame("line-######.png");

    for Hy in Hys: 
        Hy.step()
