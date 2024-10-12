from __future__ import annotations
from color import *
from dataclasses import dataclass
from enum import Enum
from typing import *

type CopyValueDef = CopyValue|tuple[CopyType, float]|Literal[0]

type AnyColorNotBlending = Color[ColorChannel]|ColorAlpha[ColorChannel]|CopyColor

type AnyColorDef = str|Color[ColorChannel]|ColorAlpha[ColorChannel]|CopyColor|BlendingColor
# type AnyColor = Color[ColorChannel]|ColorAlpha[ColorChannel]|CopyColor
type AnyColor = Color[ColorChannel]|ColorAlpha[ColorChannel]|CopyColor|BlendingColor

type GDColor = tuple[AnyColor, int]

# AnyColorVar = TypeVar("AnyColorVar", Color[ColorChannel],ColorAlpha[ColorChannel],CopyColor,BlendingColor[AnyColorNotBlending])

type ColorDesc = Tuple[AnyColorDef, str, int]
type PaletteChangeDesc = Tuple[str, list[tuple[AnyColorDef, int]]]

class CopyType(Enum):
    Offset = 1
    Factor = 2
    
@dataclass
class CopyValue:
    type: CopyType
    value: float

def resolve_copy_value(change_def: CopyValueDef) -> CopyValue:
    if isinstance(change_def, CopyValue):
        return change_def
    
    if change_def == 0:
        return CopyValue(CopyType.Offset, 0)
    
    return CopyValue(change_def[0], change_def[1])

def mul(value: float) -> CopyValue:
    return CopyValue(CopyType.Offset, value)
    
def add(value: float) -> CopyValue:
    return CopyValue(CopyType.Factor, value)

@dataclass
class CopyColor:
    copied_id: int
    h: CopyValue
    s: CopyValue
    v: CopyValue
    alpha: float
    
    @overload
    def __init__(self, change: tuple[CopyValueDef, CopyValueDef, CopyValueDef], from_id: int, /, *, a: float|None = None):
        ...
    @overload
    def __init__(self, change: tuple[CopyValueDef, CopyValueDef, CopyValueDef, float], from_id: int, /):
        ...
    
    @overload
    def __init__(self, from_id: int, /, *, a: float|None = None):
        ...
    
    def __init__(self, change_or_from_id: tuple[CopyValueDef, CopyValueDef, CopyValueDef]|tuple[CopyValueDef, CopyValueDef, CopyValueDef, float]|int, from_id: int|None = None, /, *, a: float|None = None):
        if isinstance(change_or_from_id, tuple):
            change = change_or_from_id
            assert isinstance(from_id, int)
        else:
            from_id = change_or_from_id
            change = (0, 0, 0)
            
        if isinstance(a, float):
            alpha = a
        elif len(change) == 4:
            alpha = change[3]
        else:
            alpha = 1
            
        self.copied_id = from_id
        self.h = resolve_copy_value(change[0])
        self.s = resolve_copy_value(change[1])
        self.v = resolve_copy_value(change[2])
        self.alpha = alpha

class BlendingColor:
    color: AnyColorNotBlending
    
    
    def __init__(self, color: AnyColorDef) -> None:
        if isinstance(color, str):
            color = parse_color_hex(color)
        if isinstance(color, BlendingColor):
            color = color.color
        
        # self.color = todo()
        self.color = color


# # Library
# def construct_copy_color[T](from_color: GDColor, result: Color[T]) -> CopyColor:
#     pass