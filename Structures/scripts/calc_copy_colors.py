#!/usr/local/bin/python3.12

from __future__ import annotations
from typing import *
from tabulate import tabulate 
from color import *
import colorsys
from utils import *
from enum import Enum




class NamedColor:
    name: str
    id: int
    color: Color[float]
    copy_types: ColorComponentCopyTypes|None
    
    def __init__(self, name: str, id: int, color: Color[float], copy_types: ColorComponentCopyTypes|None):
        self.name = name
        self.id = id
        self.color = color
        self.copy_types = copy_types

type RawColorDef = tuple[str, str, int] | tuple[str, str, int, ColorCopyTypesRaw]

class ColorMapping:
    base: NamedColor
    derived: Iterable[NamedColor]
    def __init__(self, base: NamedColor, derived: Iterable[NamedColor]) -> None:
        self.base = base
        self.derived = derived
        
def parse_raw_color_def(color_def: RawColorDef) -> NamedColor:
    match color_def:
        case (color_hex, name, id):
            copy_types = None
            pass
        case (color_hex, name, id, copy_types):
            copy_types = resolve_color_copy_types(copy_types)
            pass 
    
    return NamedColor(
        name=name,
        id=id,
        color=color_to_float(parse_color_hex(color_hex)),
        copy_types=copy_types,
    )

def parse_color_mapping(mapping: tuple[RawColorDef, Iterable[RawColorDef]]) -> ColorMapping:
    (base, derived) = mapping
    base = parse_raw_color_def(base)
    derived = map(parse_raw_color_def, derived)
    
    return ColorMapping(
        base=base,
        derived=derived,
    )

type RawColorMappings = Iterable[tuple[RawColorDef, Iterable[RawColorDef]]]
def parse_color_mappings(mappings: RawColorMappings) -> Iterable[ColorMapping]:
    return map(parse_color_mapping, mappings)
    # return list(map(lambda item: (parse_raw_color_def(item[0]), list(map(parse_raw_color_def, item[1]))), mappings))

class CopyType(Enum):
    Offset = 1
    Factor = 2

class CopyValue[T: (float,int)]:
    type: CopyType
    value: T
    
    def __init__(self, value: T, type: CopyType) -> None:
        self.type = type
        self.value = value
        
    def stringify(self, increment: float) -> str:
        value = round_multiple(float(self.value), increment)
        if int(value) == value:
            value = int(value)
        match self.type:
            case CopyType.Offset:
                if value > 0:
                    return f"+{value}"
                else:
                    return str(value)
            case CopyType.Factor:
                return f"x{value}"
    
    def map[R: (float,int)](self, f: Callable[[T], R]) -> CopyValue[R]:
        return CopyValue(f(self.value), self.type)

def calc_copy_value[T: float|int](base: T, derived: T, type: CopyType|None) -> CopyValue[T]:
    if type == None:
        type = CopyType.Offset if base == 0 else CopyType.Factor
    match type:
        case CopyType.Offset:
            value = derived - base
        case CopyType.Factor:
            value = derived / base
    
    return CopyValue(value, type)

class ColorComponentCopyTypes(TypedDict):
    saturation: CopyType
    brightness: CopyType

type ColorCopyTypesRaw = ColorComponentCopyTypes | CopyType

def resolve_color_copy_types(copy_types: ColorComponentCopyTypes | CopyType) -> ColorComponentCopyTypes:
    if isinstance(copy_types, CopyType):
        return {
            "saturation": copy_types,
            "brightness": copy_types
        }
    else:
        return copy_types


type ColorDiff = tuple[CopyValue, CopyValue, CopyValue]

class PopulatedColorMapping:
    base: NamedColor
    derived: Iterable[tuple[NamedColor, ColorDiff]]

def calc_diff(base: Color[float], derived: Color[float], copy_types: ColorComponentCopyTypes|None) -> ColorDiff:
    base_h, base_s, base_v = colorsys.rgb_to_hsv(*base)
    derived_h, derived_s, derived_v = colorsys.rgb_to_hsv(*derived)
    
    diff_h = calc_copy_value(base_h * 360, derived_h * 360, CopyType.Offset)
    diff_s = calc_copy_value(base_s, derived_s, map_some(copy_types, lambda types: types["saturation"]))
    diff_v = calc_copy_value(base_v, derived_v, map_some(copy_types, lambda types: types["brightness"]))
    
    
    return (
        diff_h,
        diff_s,
        diff_v,
    )
    
def populate_color_mapping(mapping: ColorMapping) -> PopulatedColorMapping:
    base = mapping.base
    def handle(color: NamedColor) -> tuple[NamedColor, ColorDiff]:
        return (color, calc_diff(base.color, color.color, color.copy_types))
    
    result = PopulatedColorMapping()
    result.base = base
    result.derived = map(handle, mapping.derived)
    return result

def calculate_diffs(mappings: Iterable[ColorMapping]) -> Iterable[PopulatedColorMapping]:
    return map(populate_color_mapping, mappings)

def print_color_mapping(mapping: PopulatedColorMapping) -> None:
    base = mapping.base
    for (derived, diff) in mapping.derived:
        names = (f"{base.name} ({base.id})", f"{derived.name} ({derived.id})")
        colors = (
            stringify_color(base.color).ljust(len(names[0])),
            stringify_color(derived.color),
        )
        names = " -> ".join(names)
        colors = " -> ".join(colors)
        print(f"For {names} ----------")
        print(f"    {colors}")
        
        (hue, saturation, brightness) = diff

        print(f"Copies:     {base.id}")
        print(f"Hue:        {hue.map(curry(wrap_range, placeholder(), -180, 180)).stringify(1)}")
        print(f"Saturation: {saturation.stringify(0.02)}")
        print(f"Brightness: {brightness.stringify(0.02)}")
        
        print("")


color_mappings: RawColorMappings = [
    (("#393840", "Wall Edge", 36), [
        ("#504f5a", "Wall Detail", 54),
        ("#211e27", "Wall Shadow Solid", 58),
        ("#403f48", "Wall Dark Main", 61),
    ]),
    (("#504f5a", "Wall Detail", 54), [
        ("#414049", "Wall Detail Border", 55),
    ]),
    (("#514f57", "Edge", 26), [
        ("#78757f", "Platform BG Main", 47),
        ("#64636b", "Platform BG Border", 48),
    ]),
    (("#efeef0", "Wall Main", 25), [
        ("#ffffff", "Plat Main", 30, {
            "saturation": CopyType.Offset,
            "brightness": CopyType.Factor
        }),
    ]),
    (("#ffc153", "Plat Accent", 27), [
        ("#e7af62", "Wall Edge Sec", 28),
    ]),
]

mappings = map(populate_color_mapping, parse_color_mappings(color_mappings))

for mapping in mappings:
    print_color_mapping(mapping)
