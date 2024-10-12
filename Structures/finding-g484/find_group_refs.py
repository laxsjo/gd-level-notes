#!/usr/local/bin/python3.12
from utils import *
from enum import Enum
from inner_level_string import parse_inner_level_str

# type Object = dict[Key, str]
    
class Key(Enum):
    OBJECT_ID = 1
    X_POSITION = 2
    Y_POSITION = 3
    SINGLE_GROUP_ID = 33
    TARGET_GROUP_ID = 51
    GROUP_IDS = 57
    SECONDARY_GROUP_ID = 71
    ANIMATION_ID = 76 # Unsure if relevant...
    GROUP_PARENT_IDS = 274
    OTHER_GROUP_ID = 457
    MIN_X_ID = 516
    MIN_Y_ID = 517
    MAX_X_ID = 518
    MAX_Y_ID = 519

group_id_keys = [Key.SINGLE_GROUP_ID, Key.TARGET_GROUP_ID, Key.SECONDARY_GROUP_ID, Key.ANIMATION_ID, Key.OTHER_GROUP_ID, Key.MIN_X_ID, Key.MIN_Y_ID, Key.MAX_X_ID, Key.MIN_Y_ID]

class Object(dict[Key, str]):
    original_str: str
    
    # This should be part of __init__
    def load_original_str(self, str: str):
        self.original_str = str
    
    def __getitem__(self, __key: Key) -> str:
        try:
            return super().__getitem__(__key)
        except KeyError:
            return "<MISSING>"

def parse_object(object_str: str) -> Object:
    key_values = {item.value for item in Key}
    def extract_key_value(pair: list[str]) -> tuple[Key, str]|None:
        property = parse_int(pair[0])
        if property != None and property in key_values:
            return (Key(property), pair[1])
        else:
            return None
    result = Object(filter(None, map(extract_key_value, as_chunks(object_str.split(","), 2))))
    # Very ugly...
    result.load_original_str(object_str)
    return result

inner_level = parse_inner_level_str("Structures.gmd")

objects = list(map(parse_object, inner_level.split(";")[1:]))

searched_for_group_id = 484

found_objects: dict[int, tuple[list[Key], Object]] = dict()

# TODO: This code is wrong because object_id is not a unique value, it is
# actually just the type of object (I think...)

for object in objects:
    for key in group_id_keys:
        value = parse_int(object[key]) if key in object else None
        if key in object and value == None:
            print(f"Invalid key {key} with value '{object[key]}'")
            
        if key in object and parse_int(object[key]) == 484:
            object_id = int(object[Key.OBJECT_ID])
            print(f"added {key}")
            if object_id in found_objects:
                found_objects[object_id][0].append(key)
            else:
                found_objects[object_id] = ([key], object)

if len(found_objects) > 0:
    for info in found_objects.values():
        object = info[1]
        print(
            f"Found group id {searched_for_group_id} in the properties {", ".join(key.name for key in info[0])}\n"
            + f"Object ID: {object[Key.OBJECT_ID]}\n"
            + f"pos: ({object[Key.X_POSITION]}, {object[Key.Y_POSITION]})"
        )
else:
    print(f"Did not find Group ID {searched_for_group_id} in the properties of any objects.")

def search_group_id_list(objects: list[Object], key: Key) -> None:
    found_objects: list[Object] = []
    for object in objects:
        if key in object:
            group_ids = map(int, object[key].split("."))
            if searched_for_group_id in group_ids:
                found_objects.append(object)

    if len(found_objects) > 0:
        for object in objects:
            print(
                f"Object with group id {searched_for_group_id} in {key}\n"
                + f"Object ID: {object[Key.OBJECT_ID]}\n"
                + f"pos: ({object[Key.X_POSITION]}, {object[Key.Y_POSITION]})"
            )
    else:
        print(f"Did not find any object with Group ID {searched_for_group_id} in {key}")

# search_group_id_list(objects, Key.GROUP_IDS)
# search_group_id_list(objects, Key.GROUP_PARENT_IDS)
