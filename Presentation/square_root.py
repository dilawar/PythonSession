import math
x = 4.0
g = 3

while not math.isclose(g*g, x):
    print( f"{g:.5f}, {g*g:.5f}, {x/g:.5f}", end=', ' )
    g = (g + x/g)/2
    print(f"{g:.5f}")
    
