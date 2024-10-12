#!/usr/local/bin/python3.12

from utils import round_multiple, num_as_minimal_type

distances = [1.6,3.5,4.4,5,5.5,-6,6,-3,3,-2.4,2.4,-1,1,-1.2,1.2,-0.5, 0.5,10,12,14,4,24,40,60,76,96,112,132,148,168,178]
# distances += [2.1, 3.9] # gd follow trigger not precise enough for these small distances :(

distance_factors = [1 + (d/40) for d in distances] + [0.5, 0.8, 0.82, 0.84, 0.95, 0.97, 1.03, 1.05, 1.06, 1.16, 1.18, 1.20, 5, 8, 12, 20, 30]

print(f"{"df":<5} {"(dist.)":<8} {"follow":<6} {"scale":<5}")
for df in distance_factors:
    distance = num_as_minimal_type(round_multiple(40 * (df - 1), 0.01))
    
    follow_mod = 1 - 1 / df
    scale = 1 / df
    
    print(f"{f"x{df}":<5} {f"(+{distance}):":<8} {round_multiple(follow_mod, 0.01):<6} {round_multiple(scale, 0.01):<5}")
    