# Hyphae base class
from functools import reduce

class Hyphae(object):
    def __init__(self, 
                 seed_points=[], 
                 bounds=(0,0,1.0,1.0), 
                 f_bounds=None):
        
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
            
            #self.draw_circle(x, y, r, DEFAULT_FILL)
        
    def draw_circle(self):
        print "draw circle not implemented"
        
    def draw_bounds(self):
        print "draw bounds not implemented" 

    def draw_branch(self, x1, y1, r1, x2, y2, r2, the):
        print "draw not implented"

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
        
        if not self.f_bounds(self.bounds, x, y): 
            return
        
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
            
            #self.draw_circle(x, y, r)
            self.draw_branch(self.X[k], self.Y[k], self.R[k], x, y, r, the)
            
            self.num += 1
