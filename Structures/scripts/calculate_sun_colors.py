#!/usr/local/bin/python3.12

from tabulate import tabulate 
from color import *

def mult_scalar[T: (int,float)](a: T, b: T) -> T:
    return a * b

mult = color_bin_op(mult_scalar)

base_color = color_to_float(parse_color_hex("ffa862"))
# base_alpha = 0.65
base_alpha = 1
base_width = 2.41

factors = [1, 0.75, 0.5, 0.25]
areas = [f ** 2 for f in factors]
alphas = [base_alpha * a for a in areas]
widths = [base_width * f for f in factors]

colors = [mult(base_color, a) for a in areas]

color_strings = [stringify_color(color_to_int(c)) for c in colors]

# I actually ended up not varying the color for different coverages, instead
# opting for keeping the color constant but instead varying the alpha. So you
# can ignore the color field

print(tabulate(zip(factors, areas, alphas, widths, color_strings), ["radius factor", "area factor", "alpha", "width", "color"]))

# base_color = 
