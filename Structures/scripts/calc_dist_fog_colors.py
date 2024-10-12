#!/usr/local/bin/python3.12

from gd_colors import *
from functools import reduce
from tabulate import tabulate
from utils import *

def composite_alphas(under: float, over: float) -> float:
    # source: https://en.wikipedia.org/wiki/Alpha_compositing#Description
    return over + under * (1 - over)

# Computes the correct copy color alpha values for a collection of stacked
# overlays, taking into acount the cumulatively added density of each layer on top. 

# this is the color at distance fog_end
fog_color = rgb("#8b729c")

density = cast(None|float, None) 
fog_end = cast(None|float, None)
# unit: fraction per block
density = 0.0008

# A layer at this distance would have an opacity of 1
# unit: blocks
# fog_end = 100

# Distances that the different stacked overlays are placed at.
distances = [2, 40, 76, 112, 148, 280, 440]

match (density, fog_end):
    case (None, None):
        panic("Must specify either density or fog_end")
    case (density, None):
        fog_end = 1 / cast(float, density)
    case (None, fog_end):
        # pass
        fog_end = fog_end
    case _:
        unreachable()

print(f"Computing for fog that ends at {fog_end} blocks")
        
alphas = []
for dist in distances:
    target_alpha = dist / fog_end
    
    current = reduce(composite_alphas, alphas, 0)
    
    # composite_alphas, but solved for over
    result = (target_alpha - current) / (1 - current)
    
    alphas.append(result)

alphas_rounded = map(lambda a: round_multiple(a, 0.01), alphas)

print(tabulate(zip(distances, alphas_rounded), ["layer dist", "alpha"]))
