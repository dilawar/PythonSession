# -*- coding: utf-8 -*-
"""
Layered implementation. 

3 layer image is used as arena. CaMKII sits on the middle layer while lower and
upper limit hosts pp1 and subunits respectively.

"""

import cv2
import numpy as np
import math
import random
import itertools
import arena
from species import CaMKII, PP1, Subunit, NMDA, dt_

time_, timeseries_ = [], []

def visualize_system( step, delay = 1, save_to_video = True):
    # redraw.
    system_ = np.zeros_like(arena.system_) + 100
    [ c.draw(system_) for c in arena.camkii_ + arena.pp1_ + arena.subunits_ + arena.nmda_]
    # in timestamp of 1e-4, particle moves on average 10nm when D = 1e-12
    activeFrac = sum([x.activeN for x in arena.camkii_])/len(arena.camkii_)/7.0

    timeseries_.append( activeFrac )
    time_.append( abs(step)*dt_ )

    hist, bins = np.histogram(timeseries_, density = True, bins = 10, range=(0,1.0))
    for i, h in enumerate(hist):
        x = 20+4*i
        y1, y2 = 0, int(10*h)
        cv2.line(system_,  (y1,x), (y2,x), 100, 2)

    msg = 't~ %.3f s| %.2f | %d' % (time_[-1], timeseries_[-1], len(arena.subunits_))
    cv2.putText(system_,msg, (0, 15), 0, 0.5, 100)
    cv2.imshow( arena.window_, system_ )
    cv2.waitKey(delay)

def ca_stimulus( arg ):
    ca = cv2.getTrackbarPos('NMDA', arena.window_)
    arena.ca_ = ca 

def make_system( arg = None ):
    # Add m system of size N each.
    arena.camkii_, arena.pp1_, arena.subunits_ = [], [], []
    arena.nmda_ = []
    arena.size_ = (2,
        #(max(cv2.getTrackbarPos('Cluster', arena.window_),0),
        cv2.getTrackbarPos('CaMKII', arena.window_))
    print("[INFO ] Building system %s, %s" % (str(arena.size_), arg))

    m, N = arena.size_
    for ni, nx in itertools.product( range(m), range(N)):
        n = ni*nx+ni
        theta = ni*math.pi*2/m+random.uniform(-math.pi/8, math.pi/8)
        r = 0.5*arena.radius_ + random.uniform(-arena.radius_/12, arena.radius_/12)
        x, y = int(r*math.cos(theta))+arena.radius_, int(r*math.sin(theta))+arena.radius_
        c = CaMKII(x, y, random.choice([0,1]))
        arena.camkii_.append(c)

        if n % 2 == 0:
            # For each camkii, there is one subunit.
            arena.subunits_.append( Subunit() )

    # And lets release 0.1 PP1 for each CaMKII. 
    for i in range( cv2.getTrackbarPos('PP1', arena.window_)):
        arena.pp1_.append( PP1() )

    # add NMDA.
    for i in range( cv2.getTrackbarPos('NMDA', arena.window_)):
        arena.nmda_.append( NMDA() )


def step( i ):
    [ x.step() for x in arena.pp1_ + arena.camkii_ + arena.subunits_ ]
    if i % 100 == 0:
        visualize_system(i, 1 )

def simuate(N):
    while N != 0:
        step(N)
        N -= 1

def plot_results():
    pass

def main():
    # create GUI and attach trackbar.
    cv2.createTrackbar('CaMKII', arena.window_, 4, 20, make_system)
    #  cv2.createTrackbar('Cluster', arena.window_, 1, 3, make_system)
    cv2.createTrackbar('PP1', arena.window_, 8, 100, make_system)
    cv2.createTrackbar('NMDA', arena.window_, 4, 10, make_system)
    #cv2.createTrackbar('ca', arena.window_, 80, 1000, ca_stimulus)

    make_system()
    simuate(-1)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print( "[INFO ] User pressed Ctrl+C" )
        cv2.destroyAllWindows()
