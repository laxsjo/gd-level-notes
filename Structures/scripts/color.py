from typing import *
from itertools import *
from utils import *
import sys
import os
import traceback

# def eprint(*args, **kwargs):
#     print(*args, file=sys.stderr, **kwargs)

# def panic(reason: str, traceback_level: int = 0) -> Never:
#     location = traceback.extract_stack()[-(traceback_level + 2)]
    
#     path = os.path.relpath(location.filename, os.getcwd())
    
#     message = f"Paniced at '{reason}'\n"
#     message += f" --> {path}:{location.lineno}"
#     if location.colno is not None:
#         message += f":{location.colno}"
#     message += f" in {location.name}"
    
#     eprint(message)
#     exit(101)

# def as_chunks[T: Sequence[Any]](iter: T, n: int) -> List[T]:
#     # cast is required because slice operation is not required to return a
#     # sequence of the same type.
#     # source: https://stackoverflow.com/a/68876155/15507414
#     return cast(List[T], [iter[i:min(i+n, len(iter))] for i in range(0, len(iter), n)])


# def parse_int(input: str, base: int = 10) -> int | None:
#     try:
#         return int(input, base=base)
#     except ValueError:
#         return None

type ColorChannel = float | int
type Color[T: ColorChannel] = Tuple[T, T, T]
type ColorAlpha[T: ColorChannel] = Tuple[T, T, T, T]

type ColorBinOp[T: ColorChannel, U: ColorChannel] = Callable[[Color[T]|T, Color[T]|T], Color[U]]
type ColorUnaryOp[T: ColorChannel, U: ColorChannel] = Callable[[Color[T]|T], Color[U]]

# Cast indeterminate length tuple into color type.
def color[T: ColorChannel](channels: tuple[T, ...]) -> Color[T]:
    return cast(Color[T], channels)

@overload
def is_color[T: ColorChannel](x: Color[T]) -> TypeGuard[Color[T]]:
    ...
    
@overload
def is_color(x: Color) -> TypeGuard[Color]:
    ...
@overload
def is_color[T: ColorChannel](x: Any) -> TypeGuard[Color[T]]:
    ...

def is_color(x) -> TypeGuard[Color]: 
    return type(x) == tuple

def color_is_type[T: Any](color: Color[Any], channel_type: type[T]) -> TypeGuard[Color[T]]:
    return type(color[0]) == channel_type \
        and type(color[2]) == channel_type \
        and type(color[1]) == channel_type

# create a binary operator taking colors based on a function that takes the two
# values of a pair of channel values.
# color_bin_op(lambda x, y: x + y)((50, 50, 25), (25, 25, 25)) = (75, 75, 50)
# color_bin_op(lambda x, y: x + y)((50, 50, 25), 25) = (75, 75, 50)
def color_bin_op[T: ColorChannel, U: ColorChannel](func: Callable[[T, T], U]) -> Callable[[Color[T] | T, Color[T] | T], Color[U]]:
    def elevate_to_color(a: Color[T] | T) -> Color[T]:
        match a:
            case (_, _, _):
                return a
            case _:
                return (a, a, a)
        
    def op(a: Color[T] | T, b: Color[T] | T) -> Color[U]:
        return color(tuple(starmap(func, zip(elevate_to_color(a), elevate_to_color(b)))))
    
    return op

# create a unary color operator based on function operating on individual
# channels.
def color_unary_op[T: ColorChannel, U: ColorChannel](func: Callable[[T], U]) -> Callable[[Color[T]|T], Color[U]]:
    def elevate_to_color(a: Color[T] | T) -> Color[T]:
        match a:
            case (_, _, _):
                return a
            case _:
                return (a, a, a)
    
    return (lambda a:
        cast(Color, tuple(map(func, elevate_to_color(a))))
    )

def color_to_int(col: Color[float]) -> Color[int]:
    return color_unary_op(lambda x: int(round(x * 255.0)))(col)

# Convert color from integer 0-255 to float 0.0-1.0 form.
def color_to_float(col: Color[int]) -> Color[float]:
    # For worries about interval ranges size mismatches, see
    # https://stackoverflow.com/a/46575472/15507414.
    return color_unary_op(lambda x: float(x) / 255.0)(col)

def parse_color_hex(hex: str) -> Color[int]:
    stripped = hex.strip("#")
    
    components = tuple(map(lambda x: int(x, 16), as_chunks(stripped, 2)))
    
    if len(components) != 3:
        panic(f"Invalid color code '{hex}'. Color must have 3 components, {len(components)} found.")
    
    return components
    
# ex: parse_color_rgb("rgb(0, 50, 255)") = (0, 50, 255)
def parse_color_rgb(rgb: str) -> Color[int]:
    def parse_component(raw: str) -> int:
        component = parse_int(raw.strip())
        if component is None:
            panic(f"Invalid rgb component '{raw.strip()}' in '{rgb}'")
        
        return component
        
    components = tuple(map(parse_component, rgb.removeprefix("rgb(").removesuffix(")").split(",")))
    if len(components) != 3:
        panic(f"Invalid rgb color '{rgb}'. Color must have 3 components, {len(components)} found.")
    
    return components

@overload
def rgb[T: ColorChannel](hex: str, /) -> Color[int]:
    ...

@overload
def rgb[T: ColorChannel](r: T, g: T, b: T, /) -> Color[T]:
    ...
    
def rgb[T: ColorChannel](r_or_hex: str|T, g: T|None = None, b: T|None = None, /) -> Color[T]:
    if isinstance(r_or_hex, str):
        # Cast is safe because this overload path always returns an int color
        return cast(Any, parse_color_hex(r_or_hex))
    elif g == None or b == None:
        panic(f"Nonexistant Overload: invalid type combination, r_or_hex={r_or_hex}, g={g}, b={b}")
    else:
        return (r_or_hex, g, b)

@overload
def rgba[T: ColorChannel](hex: str, a: T, /) -> ColorAlpha[T]:
    ...
    
@overload
def rgba[T: ColorChannel](r: T, g: T, b: T, a: T, /) -> ColorAlpha[T]:
    ...

def rgba[T: ColorChannel](r_or_hex: str|T, g_or_a: T, b: T|None = None, a: T|None = None, /) -> ColorAlpha[T]:
    if isinstance(r_or_hex, str):
        color = parse_color_rgb(r_or_hex)
        if isinstance(g_or_a, float):
            color = color_to_float(color)
        # This cast is dangerous if the definition of ColorChannel ever changes!!
        r_res, g_res, b_res = cast(Color[T], color)
        a_res = g_or_a
    elif b == None or a == None:
        panic(f"Nonexistant Overload: invalid type combination, r_or_hex={r_or_hex}, g_or_a={g_or_a}, b={b}, a={a}")
    else:
        r_res, g_res, b_res = r_or_hex, g_or_a, b
        a_res = a
    
    return (r_res, g_res, b_res, a_res)

def stringify_color[T: ColorChannel](color: Color[T]) -> str:
    if color_is_type(color, float):
        c_int = color_to_int(color)
    elif color_is_type(color, int):
        c_int = color
    else:    
        panic("unreachable")
    
    c = cast(Color[int], tuple(map(lambda x: max(x, 0), c_int)))
    return "#" + f"{c[0]:02x}{c[1]:02x}{c[2]:02x}"

def stringify_color_rgb(color: Color) -> str:
    if color_is_type(color, float):
        c_int = color_to_int(color)
    elif color_is_type(color, int):
        c_int = color
    else:    
        panic("unreachable")
    
    return f"rgb({c_int[0]}, {c_int[1]}, {c_int[2]})"