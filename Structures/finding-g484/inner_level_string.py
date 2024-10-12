#!/usr/local/bin/python3.12

import lxml.etree as ET
import base64
import gzip
import io
from utils import *

def parse_inner_level_str(gmd_file_path: str) -> str:
    with open(gmd_file_path, "r") as file:
        try:
            tree = ET.parse(file)
        except ET.ParseError as parse_error:
            message = f"Failed to parse: {parse_error.msg}\n"
            message += f" --> {gmd_file_path}:{parse_error.position[0]}:{parse_error.position[1]}"
            
            panic(message)
    
    match tree.xpath("dict/k[text()=\"k4\"]/following-sibling::s[1]/text()"):
        case [str(content)]:
            result = content
        case other:
            panic(f"Got invalid result '{other}' from pattern")
    result = base64.b64decode(result, altchars="-_")
    result = gzip.decompress(result).decode()
    
    return result