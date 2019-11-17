
from functools import reduce

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

class Hyphae():
    def __init__(self, 
                 seed_points=[], 
                 bounds=(0,0,1.0,1.0), 
                 f_bounds=in_square):
        
        self.bounds = bounds
        self.f_bounds = f_bounds
        
        self.NMAX = int(2*1e4)
        self.SIZE = 800
        self.ONE = 1. / self.SIZE
        self.RAD = 12. * self.ONE
        self.ZONEWIDTH = 1. * (self.RAD / self.ONE)
        self.ZONES = int(self.SIZE / self.ZONEWIDTH)
        
        self.RAD_SCALE = 0.86
        self.SEARCH_ANGLE_MAX = 1.5 * PI
        self.R_RAND_SIZE = 60
        self.CK_MAX = 10
        
        self.WEIGHT = 3 / self.RAD
        
        self.COLOR = (232, 158, 223)
        self.GCOLOR = 158
        
        self.SOURCE_NUM = 12
        
        self.Z = [[] for i in range((self.ZONES+2)**2)]
        
        self.R = [0. for x in range(self.NMAX)]
        self.X = [0. for x in range(self.NMAX)]
        self.Y = [0. for x in range(self.NMAX)]
        self.THE = [0. for x in range(self.NMAX)]
        self.GE = [0. for x in range(self.NMAX)]
        self.P = [0 for x in range(self.NMAX)]
        self.C = [0 for x in range(self.NMAX)]
        self.D = [-1 for x in range(self.NMAX)]
        
    
        self.i = 0
        
        self.num = self.SOURCE_NUM
        
        #for j in range(self.SOURCE_NUM):
        for j,(x,y) in enumerate(seed_points):
            #x = random(0.1, 0.9)
            #y = random(0.1, 0.9)
            
            #print(self.ONE, x, y)
            
            self.X[j] = x
            self.Y[j] = y
            # self.R[j] = (self.RAD + 0.2 * self.RAD * (1. - 2. * random(1.)))
            self.R[j] = self.RAD
            self.P[j] = -1
            
            self.THE[j] = random(1.) * PI * 2.
            self.GE[j] = 1
            self.P[j] = self.RAD
            z = self.get_z(self.X[j], self.Y[j])
            self.Z[z].append(j)
            
            r = self.R[j]
            
            self.draw_circle(x, y, r, DEFAULT_FILL)
        
    def draw_bounds(self):
        if len(self.bounds) == 3:
            """
            stroke(255)
            strokeWeight(3)
            
            x,y,r = self.bounds
            
            print("drawing bounds:", self.bounds, int(x * XMAX), int(y * YMAX), int(r*XMAX))
            circle(int(x * XMAX), int(y * YMAX), int((r*2)*XMAX))
            """
            x,y,r = self.bounds 
            r *= 2
            
            gradient_ring(int(x*XMAX), 
                          int(y*YMAX), 
                          int(r*XMAX), 
                          int(r*XMAX)+50, 
                          color(255,255,255), 
                          color(0,0,0))
    
    def smooth_c_line(self, x1, y1, r1, x2, y2, r2, the):
        stroke(255)
        #strokeWeight(4)

        self.draw_line(x1, y1, x2, y2, r2)
        #self.grad_line(x1, y1, r1, x2, y2, r2, the)
        return
        #print(x1, y1, r1, x2, y2, r2, the)
        
        r,g1,b = DEFAULT_FILL
        _,g2,_ = DEFAULT_FILL
        
        g1 = (100 * r1) + 120
        g2 = (100 * r2) + 120
        
        delta = 1.0 / min(XMAX, YMAX)
        
        d = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        nsteps = int(d / delta)
        for i in range(1, nsteps):
            step = i * delta
            nx = x1 + sin(the) * step 
            ny = y1 + cos(the) * step
            nr = (1 - (i / nsteps)) * r1
            ng = g1 + ((i/nsteps) * (g2-g1))
                  
            self.draw_circle(nx, ny, nr, (r, ng, b))
        
        self.draw_circle(x2, y2, r2, (r, g2, b))

    def draw_line(self, x1, y1, x2, y2, r, col=None):
        if col:
            stroke(col)
        strokeWeight((self.WEIGHT * r) + 1)
        line(int(x1 * XMAX), int(y1 * YMAX), int(x2 * XMAX), int(y2 * YMAX))
        
    def grad_line(self, x1, y1, r1, x2, y2, r2, the):
        delta = 1.0 / min(XMAX, YMAX)
        d = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        nsteps = int(d / delta)

        r,g1,b = self.COLOR
        _,g2,_ = self.COLOR
        
        g1, g2 = self.GCOLOR * r1, self.GCOLOR * r2
                    
        c1, c2 =  color(r, g1, b), color(r, g2, b)
        
        px, py = x1, y1
        for i in range(1, nsteps):
            step = i * delta
            nx = x1 + sin(the) * step 
            ny = y1 + cos(the) * step
            nr = (1 - (i / nsteps)) * r1
            ng = g1 + ((i/nsteps) * (g2-g1))
                
            self.draw_line(px, py, nx, ny, nr, lerpColor(c1, c2, 1 - (i / nsteps)))
            
            px, py = nx, ny
            
    
    def draw_circle(self, x, y, rad, rgb):
        fill(*rgb)
        circle(int(x * XMAX), int(y * YMAX), rad * 450.)
    
    def near_zone_inds(self, x, y):
        i = 1 + int(x * self.ZONES)
        j = 1 + int(y * self.ZONES)
        iss = [i-1, i, i+1, i-1, i, i+1, i-1, i, i+1]
        jss = [j+1, j+1, j+1, j, j, j, j-1, j-1, j-1]
        ij = [a * self.ZONES + b for a,b in zip(iss, jss)]
        
        its = [self.Z[a] for a in ij]
        inds = [b for a in its for b in a]
        
        return inds
    
    def get_z(self, x, y):
        i = 1 + int(x * self.ZONES)
        j = 1 + int(y * self.ZONES)
        z = i * self.ZONES + j
        return z
    
    def step(self):
        k = int(random(self.num))
        
        # print("k - ", k)
        
        self.C[k] += 1
    
        if self.C[k] > self.CK_MAX:
            return
    
        r = self.R[k] * self.RAD_SCALE if self.D[k] > -1 else self.R[k]
        
        if r < 4 * self.ONE:
            self.C[k] = self.CK_MAX + 1
            return
        
        ge = self.GE[k] + 1 if self.D[k] > -1 else self.GE[k]
        the = self.THE[k] + (1.-1. / ((ge+1)**0.1)) * randomGaussian() * self.SEARCH_ANGLE_MAX
        
        x = self.X[k] + sin(the) * r
        y = self.Y[k] + cos(the) * r
        
        #if x > 1.000000 or x < 0.000000: return
        #if y > 1.000000 or y < 0.000000: return
        
        if not self.f_bounds(self.bounds, x, y): return
        
        try:
            inds = self.near_zone_inds(x, y)
            inds = [a for a in inds if not a==k and not a==self.P[k]]
        except IndexError:
            return
        except TypeError:
            return
        
        good = True
        if len(inds) > 0:
            dd = [(self.X[ind] - x)**2 + (self.Y[ind] - y)**2 for ind in inds]
            dd = list(map(lambda d: sqrt(d), dd))
            
            msk = [d*2 > self.R[ind] + r for d, ind in zip(dd, inds)]
            good = reduce(lambda a,b: a and b, msk)
        
        if good:
            self.X[self.num] = x
            self.Y[self.num] = y
            self.R[self.num] = r
            self.THE[self.num] = the
            self.P[self.num] = k
            self.GE[self.num] = ge
            
            if self.D[k] < 0:
                self.D[k] = self.num
                
            z = self.get_z(x, y)
            self.Z[z].append(self.num)
            
            # print(int(x * XMAX), int(y * YMAX))
            #self.draw_circle(x, y, r)
            self.smooth_c_line(self.X[k], self.Y[k], self.R[k], x, y, r, the)
            
            self.num += 1

def tri_points(x,y,h):
    return [
        (x , y - (h/2)),
        (x - (h/2), y + (h/2)),
        (x + (h/2), y+ (h/2))
    ]


# move G to 228
DEFAULT_FILL = (230, 228, 235)
x = 0

Hys = []
Hy = None
Hy2 = None
def setup():
    size(XMAX, YMAX)
    
    
    frameRate(800)
    background(0)
    smooth()
 
    #noStroke()
    fill(*DEFAULT_FILL)
 
    global Hys
    
    Hys.append(Hyphae(seed_points=tri_points(0.25,0.25,0.1),
                      bounds=(0.25, 0.25, 0.2), 
                      f_bounds=in_circle))
    Hys.append(Hyphae(seed_points=tri_points(0.75,0.25,0.1),
                      bounds=(0.75, 0.25, 0.2), 
                      f_bounds=in_circle))
    Hys.append(Hyphae(seed_points=tri_points(0.50,0.75,0.1),
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
    
    n_x = mouseX
    if abs(n_x - x) > 5:
        #print(n_x)
        pass
        
