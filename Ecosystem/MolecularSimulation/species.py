import cv2
import random
import arena
import math

rate_pick_subunit_  = 0.001
rate_loose_subunit_ = 0.001
dt_ = 1e-5

def r_of_phospho():
    # in uM.
    ca =  arena.ca_ + random.uniform(0, 15)
    kh1 = 0.7
    r = ((ca/kh1)**3 / (1+(ca/kh1)**3))**2 * dt_
    return r

class CaMKII():
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.symm = random.choice([6,7])
        self.activeN = 0
        self.move = True
        self.attachedNMDAIndex = -1
        print( 'camkii: symm=%d' % self.symm )

    def draw(self, img, simple = False):
        if simple:
            fill = -1
            if self.activeN > 1:
                fill = -1

            color = 100 + 20*self.activeN
            cv2.circle(img, (self.y,self.x), 5, (0,color,0), fill)
            t = '%d/%d' % (self.activeN, self.symm)
            cv2.putText(img, t, (self.y+5, self.x+5), 0, 0.3, (0,255,0))
            return

        # Else draw hexagonals.
        r, dtheta = 8, 2 * math.pi / self.symm
        color = 255
        for i in range(self.symm):
            fill = 0
            if i < self.activeN:
                fill = -1
            theta = i * dtheta
            center = (int(self.y+r*math.cos(theta)), int(self.x+r*math.sin(theta)))
            cv2.circle( img, center, 4, (0,color,0), fill)
            t = '%d' % (self.symm,)
            cv2.putText(img, t, (self.y+5, self.x+5), 0, 0.3, (0,255,0))

    def diffuse(self):
        if not self.move:
            return

        if random.random() < 0.5:
            self.x += -1 if random.random() < 0.5 else 1
        else:
            self.y += -1 if random.random() < 0.5 else 1

        self.x = self.x % 500
        self.y = self.y % 500


    def step( self ):
        # check if any NMDA receptor is in my vicinity. attach to it only if I
        # am active.
        if self.activeN > 2:
            nmdaIdx = arena.isAnyNMDANearby(self.x, self.y, 10, maxAttach = 2)
            if nmdaIdx > -1:
                self.move = False
                self.attachedNMDAIndex = nmdaIdx
                arena.nmda_[nmdaIdx].numCaMKIIAttached += 1
        else:
            # Inactive camkii always moves.  If it was attached to any NMDA
            # receptor, starts moving now.
            self.move = True
            arena.nmda_[self.attachedNMDAIndex].numCaMKIIAttached -= 1
            self.attachedNMDAIndex = -1

        if self.symm == 7:
            # Release a subunit with probability 0.1
            if random.random() < rate_loose_subunit_:
                # Type of subunit which is lost.
                isLostSubunitActive = True if random.random() < (self.activeN/self.symm) else False
                self.symm -= 1
                if isLostSubunitActive:
                    self.activeN -= 1
                #  print('Release subunit ', end = '' )
                x = Subunit( self.x + 10, self.y + 10, isLostSubunitActive )
                arena.subunits_.append( x )
        else:
            # Now it can gain a subunit. 
            # Check if there is a subunit in its neighbourhood.
            xindex = arena.isAnySubunitNearby(self.x, self.y, 10)
            if xindex > -1:
                # subunit is picked up
                if random.random() < rate_pick_subunit_:
                    self.symm += 1
                    # If picked up unit is active, this holoenzyme becomes
                    # active.
                    if arena.subunits_[xindex].active:
                        self.activeN += 1
                    # and the subunit disappear
                    del arena.subunits_[xindex]

        # At basal calcium.
        r = r_of_phospho()
        # If more than 0 subunits are already phosphorylated then further
        # phosphorylation is pretty fast.
        if self.activeN > 0:
            r = r ** 0.5

        #  print( r)
        inactive = self.symm - self.activeN
        assert inactive >= 0
        if inactive > 0 and random.random() < inactive * r:
            self.activeN += 1

        self.diffuse()


class PP1():
    def __init__(self):
        self.x = int(random.uniform(0,500))
        self.y = int(random.uniform(0,500))
        self.active = True
        self.move = True
        self.complexSubunit = -1
        self.complexCaMKII = -1

    def draw(self, img):
        t = 'p'
        if self.active:
            cv2.putText(img, t, (self.y,self.x), 0, 0.5, (255,0,0), 2)
        else:
            cv2.putText(img, t, (self.y, self.x), 0, 0.5, (100,0,0), 2)

    def step(self):
        if self.move:
            d = 0 if random.random() < 0.5 else 1
            if d == 0:
                self.x +=  -1 if random.random() < 0.5 else 1
            else:
                self.y += -1 if random.random() < 0.5 else 1 

            self.x = self.x % 500
            self.y = self.y % 500

        # Now check if any active subunit is close to me.
        if self.move:
            xindex = arena.isAnySubunitNearby(self.x, self.y, 5)
            if xindex > -1:
                # This subunit is dephosphorylated immediately or with very high
                # probability. make a complex immediately
                self.move = False
                arena.subunits_[xindex].move = False
                self.complexSubunit = xindex

            # check if any camkii is nearby.
            cindex = arena.isAnyActiveCaMKIINearby(self.x, self.y, 10 )
            if cindex > -1:
                self.move = False
                self.complexCaMKII = cindex

        # if PP1 is not moving, then definately it is attached to either subunit
        # or holoenzymes.
        if not self.move:
            if self.complexSubunit > -1:
                if random.random() < 0.1:
                    try:
                        arena.subunits_[self.complexSubunit].active = False
                        arena.subunits_[self.complexSubunit].move = True
                    except Exception as e:
                        #  print( e, self.complexSubunit, arena.subunits_ )
                        print( "[ERROR] Could not track a subunit. Due to float-> int error?" )
                    self.move = True
                    self.complexSubunit = -1

            elif self.complexCaMKII > -1:
                pr = 0.1
                if not arena.camkii_[self.complexCaMKII].move:
                    pr = 0.001

                if random.random() < pr:
                    if arena.camkii_[self.complexCaMKII].activeN > 0:
                        arena.camkii_[self.complexCaMKII].activeN -= 1
                    else:
                        # When no subunit on attached camkii remained active,
                        # detach and move
                        self.complexCaMKII = -1
                    self.move = True

class Subunit():

    def __init__(self, x = None, y = None, active = None):
        self.x = x or int(random.uniform(0,500))
        self.y = y or int(random.uniform(0,500))
        self.active = active or random.choice([0, 1])
        self.move = True
        #  print( '   ... created', len(arena.subunits_) )

    def draw(self, img):
        fill = -1 if self.active else 0
        #  t = '*' if self.active else 'o'
        #  cv2.putText(img, t, (self.y, self.x), 0, 0.3, (0,255,0))
        cv2.circle( img, (self.y, self.x), 3, (0,255,0), fill )

    def step(self):
        if self.move:
            if random.random() < 0.5:
                self.x +=  -1 if random.random() < 0.5 else 1
            else:
                self.y += -1 if random.random() < 0.5 else 1 
            self.x = self.x % 500
            self.y = self.y % 500

        # Given the basal calcium level, each subunit has probability of
        # becoming active.
        if not self.active:
            if random.random() < r_of_phospho():
                self.active = True


class NMDA():

    def __init__(self, x = None, y = None ):
        self.x = x or int(random.uniform(50, 450))
        self.y = y or int(random.uniform(50, 450))
        self.numCaMKIIAttached = 0

    def draw(self, img):
        cv2.circle(img, (self.y, self.x), 10, (255,255,0) )
        cv2.putText(img, 'NMDA', (self.y, self.x), 0, 0.3, (0,255,0))
