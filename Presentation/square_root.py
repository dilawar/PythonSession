import math

x = 4.0
g = 3

while not math.isclose(g*g, x):
    print( f"{g:.2f}, {g*g:.5f}, {x/g:.5f}", end=', ' )
    #print(g, g*g, x/g)
    g = (g + x/g)/2
    print(f"{g:.5f}")
    
