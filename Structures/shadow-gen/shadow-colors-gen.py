#!/usr/local/bin/python3.12
# pyright: reportCallIssue=false, reportInvalidTypeVarUse=false

# This script generates shadowed colors and generates a new svg file based on
# the manually edited svg file. This was done to to make it easier to quickly
# preview different shadowing functions.

import sys
from typing import *
from itertools import *
import itertools
# import xml.etree.ElementTree as ET
import re
import inspect
import functools
import traceback
import os
import lxml.etree as ET
import colorsys
import math
from tabulate import tabulate
from ..scripts.color import *
from ..scripts.utils import *

def save_svg(tree: ET._ElementTree, path: str):
    tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f'Saved result to "{path}"')
    # with open(path, "w") as f:

# Replace tag namespace URI with it's name base on provided namespace mapping.
def resolve_ns(tag: str, name_space: dict[str, str]) -> str:
    match = re.search(r"^{(.*)}(.*)$", tag)
    if match is None:
        # Tag has no namespace
        return tag
    
    compose((tuple, reversed))
    reversed((4, 2))
    
    uri = match.group(1)
    tag_name = match.group(2)
    
    uri_name_spaces = dict(map(compose((list, reversed)), name_space.items()))
    if uri not in uri_name_spaces:
        panic(f"invalid uri in element tag '{tag_name}', name not defined")
    name = uri_name_spaces[uri]
    
    if name == "":
        return tag_name
    else:
        return f"{name}:{tag_name}"

class PopulatedColorEntry:
    name: str
    base_id: str
    base_gd_id: int|None
    base_color: Color[int]
    shadow_id: str
    shadow_gd_id: int|None
    shadow_color: Color[int]

class ColorEntry:
    base_id: str
    shadow_id: str
    
    def __init__(self, base_id: str, shadow_id: str) -> None:
        self.base_id = base_id
        self.shadow_id = shadow_id
    
    def populate(self, name: str, base_gd_id: int|None, base_color: Color[int], shadow_gd_id: int|None, shadow_color: Color[int]) -> PopulatedColorEntry:
        result = PopulatedColorEntry()
        
        result.base_id = self.base_id
        result.shadow_id = self.shadow_id
        
        
        result.name = name
        result.base_gd_id = base_gd_id
        result.base_color = base_color
        result.shadow_color = shadow_color
        result.shadow_gd_id = shadow_gd_id
        
        return result

def parse_color_structure(structure: dict[str, tuple[str, str]]) -> dict[str, ColorEntry]:
    return {
        base_id: ColorEntry(
            base_id,
            shadow_id
        )
        for base_id, (base_color, shadow_id) in structure.items()
    }

# The function used to compute the shadow colors
def darken_color(col: Color[int]) -> Color[int]:
    
    col_float = color_to_float(col)
    
    c_sub: ColorBinOp[float, float] = color_bin_op(lambda a, b: a - b)
    c_mul: ColorBinOp[float, float] = color_bin_op(lambda a, b: a * b)
    c_sq: ColorUnaryOp[float, float] = color_unary_op(lambda a: a ** 2)
    
    darken_factor = 0.90
    
    h, l, s = colorsys.rgb_to_hls(*col_float)
    l **= 1.2
    l *= darken_factor
    s **= 1.2
    s *= 0.9 ** 3
    
    return color_to_int(colorsys.hls_to_rgb(h, l, s))
    # return color_to_int(c_sq(col_float))

# Namespaces (why doesn't ElementTree expose any way to parse the used
# namespaces dynamically??)
NS = {
    "": "http://www.w3.org/2000/svg",
    "xlink": "http://www.w3.org/1999/xlink",
    "bx": "https://boxy-svg.com",
}

# color_def should be a valid 'linearGradient' color def element.
def set_def_color(tree: ET._ElementTree, id: str, color: Color) -> None:
    
    path = f"defs/linearGradient[@id='{id}']/stop"
    stop = expect(tree.find(path, NS), f"'stop' element under 'linerGradient' color definition element with path {path} not found")
    style = expect(stop.get("style"), "expect stop element to have style attribute")
    stop.set(
        "style",
        re.sub(r"stop-color:\s+rgb\([^)]*\)", f"stop-color: {stringify_color_rgb(color)}", style)
    )
def get_def_name(tree: ET._ElementTree, id: str) -> tuple[str, int|None]:
    path = f"defs/linearGradient[@id='{id}']/title"
    title = expect(tree.findtext(path, namespaces=NS), f"expect 'title' element under 'linerGradient' color definition element with path {path} to exist")
    
    match = expect(re.search(r"([^(\n\r]*)(?:\(([^)\n\r]+)\))?", title), f"expect title text '{title}' to match")
    name = expect(cast(str|None, match.group(1)), "expect match to contain at least one group")
    gd_id = map_some(cast(str|None, match.group(2)), parse_int)
    
    return (name, gd_id)
def get_def_color(tree: ET._ElementTree, id: str) -> Color[int]:
    path = f"defs/linearGradient[@id='{id}']/stop"
    stop = expect(tree.find(path, NS), f"expect 'stop' element under 'linerGradient' color definition element with path {path} to exist")
    rgb = expect(
        re.search(r"stop-color:\s+(rgb\([^)]*\))", stop.get("style") or ""),
        "expect stop element to contain 'style' attribute with 'stop-color: rgb(...)'"
    ).group(1)
    
    return parse_color_rgb(rgb)

def populate_colors(tree: ET._ElementTree, colors: dict[str, ColorEntry]) -> list[PopulatedColorEntry]:
    defs_el = tree.find("defs", NS)
    if defs_el is None:
        panic("No 'defs' element found :(")
    
    elements = list(filter(
        lambda el:
            resolve_ns(el.tag, NS) == "linearGradient"
            and el.get("id") in colors,
        defs_el.iterfind("./*", NS)
    ))
    
    found_ids = set(map(curry(ET._Element.get, placeholder(), "id"), elements))
        
    missing_ids = set(colors.keys()) - found_ids
    
    if len(missing_ids) != 0:
        panic(f"not all lit color ids found, missing {missing_ids}")
    
    def populate(entry: ColorEntry) -> PopulatedColorEntry:
        (name, base_gd_id) = get_def_name(tree, entry.base_id)
        base_color = get_def_color(tree, entry.base_id)
        
        
        (_, shadow_gd_id) = get_def_name(tree, entry.shadow_id)
        shadow_color = darken_color(base_color)
        
        return entry.populate(name, base_gd_id, base_color, shadow_gd_id, shadow_color)
    
    
    entries = list(map(populate, colors.values()))
    return entries

def apply_colors(tree: ET._ElementTree, colors: list[PopulatedColorEntry]):
    def unpack_entry(entry: PopulatedColorEntry) -> list[tuple[str, Color]]:
        return [(entry.base_id, entry.base_color), (entry.shadow_id, entry.shadow_color)]
        
    mappings = flatten(map(unpack_entry, colors))
    
    for id, color in mappings:
        set_def_color(tree, id, color)

def print_colors(colors: list[PopulatedColorEntry]):
    def entry_to_row(entry: PopulatedColorEntry):
        return [
            entry.name,
            stringify_color(entry.base_color) + f" ({entry.base_gd_id})" if entry.base_gd_id else "",
            "-->",
            stringify_color(entry.shadow_color) + f" ({entry.shadow_gd_id})" if entry.shadow_gd_id else ""
        ]
    
    headers = ["", "Lit", "", "Shadowed"]
    data = [
        entry_to_row(entry)
        for entry in colors
    ]
    print("Resulting Color Mappings:")
    print(tabulate(data, headers, colalign=("right",)))
    print("")

def handle_svg(tree: ET._ElementTree, colors: dict[str, ColorEntry]) -> ET._ElementTree:
    calculated_colors = populate_colors(tree, colors)
    
    apply_colors(tree, calculated_colors)
    
    print_colors(calculated_colors)
    
    return tree


def main() -> None:
    # Color definitions:
    # entry = `lit_id: (lit_hex, shadow_id)`
    colors = {
        # Wall Edge
        "color-14": ("#393840", "color-21"),
        
        # Plat Main
        "color-10": ("#ededed", "color-20"),
        
        # Wall Edge Sec
        "color-8": ("#d7b372", "color-19"),
        
        # Wall Accent
        "color-9": ("#ffc153", "color-18"),
        
        # Edge
        "color-6": ("#514f57", "color-17"),
        
        # Wall Main
        "color-5": ("#d3cfce", "color-16"),
    }
    
    path = "../decoration.svg"

    with open(path, "r") as file:
        try:
            tree = ET.parse(file)
        except ET.ParseError as parse_error:
            message = f"Failed to parse: {parse_error.msg}\n"
            message += f" --> {path}:{parse_error.position[0]}:{parse_error.position[1]}"
            
            panic(message)

    result = handle_svg(tree, parse_color_structure(colors))
    
    save_svg(result, "generated.svg")

    print("success!")
        
if __name__ == '__main__':
    main()