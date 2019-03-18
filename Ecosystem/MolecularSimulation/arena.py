"""arena.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import numpy as np
import cv2

size_     = (1, 4)        # System size (m,N); m switch with N holoenzymes
radius_   = 250           # Radius/domain of arena. 5px = 1nm
system_   = np.zeros( shape=(2*radius_,2*radius_,3), dtype=np.uint8 )
camkii_   = []
pp1_      = []
subunits_ = []
nmda_     = []

# in micro molar
ca_       = 80

def callback():
    pass

# setup window.
window_ = "PSD"
cv2.namedWindow( window_ )

def getNeighbourhood( x, y, r ):
    global system_
    return system_[x-r:x+r,y-r:y+r,:]

def dist( p1, p2 ):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def isAnySubunitNearby(x, y, r):
    for i, sub in enumerate(subunits_):
        if not sub.move:
            # This is already attached to some other PP1
            continue
        if dist( (x,y), (sub.x, sub.y)) < r:
            return i
    return -1

def isAnyActiveCaMKIINearby(x, y, r, notattachedToNMDA = False):
    for i, cam in enumerate(camkii_):
        if cam.activeN == 0:
            continue

        if notattachedToNMDA:
            if cam.attachedNMDAIndex > -1:
                continue

        if dist( (x,y), (cam.x, cam.y)) < r:
            return i
    return -1

def isAnyNMDANearby(x, y, r, maxAttach = 2):
    for i, nmda in enumerate(nmda_):
        if nmda.numCaMKIIAttached >= maxAttach:
            continue
        if dist( (x,y), (nmda.x, nmda.y)) < r:
            return i
    return -1

