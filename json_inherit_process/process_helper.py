from .processers.extend import process_extend
from .processers.relative import process_relative
from .processers.proportional import process_proportional
from .processers.delete import process_delete
import copy
import os
import json

item_types = ["GENERIC", "AMMO", "MAGAZINE", "ARMOR", "TOOL", "PET_ARMOR",
              "BOOK", "BIONIC_ITEM", "COMESTIBLE", "GUN", "GUNMOD", "BATTERY", "TOOL_ARMOR"]


def need_wait(json_objects: list) -> bool:
    for json_object in json_objects:
        if type(json_object) is int:
            return True
    return False


def dump_json(json_objects: list, out_file: str):
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(os.path.dirname(out_file))
    json.dump(json_objects, open(out_file, mode="w",
                                 encoding="utf-8"), ensure_ascii=False, indent=2)


def process_json_inheritance(sub_json_object: dict, super_json_object: dict):
    if super_json_object == None:
        print(
            "WARR no super,copy-from is {},type is {}".format(sub_json_object["copy-from"], sub_json_object["type"]))
        processed_json_object = {}
    else:
        processed_json_object = copy.deepcopy(super_json_object)

    id_parts = ["id", "result", "id_suffix", "abstract"]
    for id_part in id_parts:
        if id_part in processed_json_object:
            del processed_json_object[id_part]

    if "MONSTER_FACTION" == get_json_type_str(processed_json_object):
        del processed_json_object["name"]

    # sub json have look like super
    if "id" in processed_json_object:
        processed_json_object["looks_like"] = processed_json_object["id"]

    inherit_templet = copy.deepcopy(sub_json_object)

    if "copy-from" in inherit_templet:
        del inherit_templet["copy-from"]

    process_extend(processed_json_object, inherit_templet)
    process_delete(processed_json_object, inherit_templet)
    process_proportional(processed_json_object, inherit_templet)
    process_relative(processed_json_object, inherit_templet)

    for key, value in inherit_templet.items():
        processed_json_object[key] = value

    return processed_json_object


def equal_id(super_id: str, super_ids):
    if type(super_ids) is str:
        return super_id == super_ids
    elif type(super_ids) is list:
        return super_id in super_ids
    elif super_ids == None:
        return False
    else:
        raise Exception("Wrong id type is ", type(super_ids))


def get_json_type_str(json_object: dict) -> str:
    if "type" not in json_object:
        return None
    json_type = json_object["type"]
    if json_type in item_types:
        json_type = "item_type"
    return json_type


def get_json_id_str(json_object: dict) -> str:
    result = None
    if "id" in json_object:
        result = json_object["id"]
    elif "result" in json_object:
        if "id_suffix" in json_object:
            result = json_object["result"] + "_" + json_object["id_suffix"]
        else:
            result = json_object["result"]
    elif "abstract" in json_object:
        result = json_object["abstract"]
    elif "MONSTER_FACTION" == get_json_type_str(json_object):
        result = json_object["name"]
    return result


def add_json_to_processed_json_list_dict(json_object: dict, processed_json_list_dict: dict):
    json_type = get_json_type_str(json_object)
    if json_type in processed_json_list_dict.keys():
        processed_json_list_dict[json_type].append(json_object)
    else:
        processed_json_list_dict[json_type] = [json_object]


def find_super_json(super_id: str, json_type: str, processed_json_list_dict: dict) -> dict:
    if json_type in item_types:
        json_type = "item_type"
    if json_type in processed_json_list_dict.keys():
        for processed_json_object in processed_json_list_dict[json_type][::-1]:
            if super_id == get_json_id_str(processed_json_object):
                return processed_json_object
    return None


def test():
    sub = {
        "id": "sub",
        "type": "one",
        "extend": {
            "flags": "flags3"
        },
        "delete": {
            "flags": "flags1"
        },
        "proportional": {
            "num1": 0.2
        },
        "relative": {
            "num": 10
        }
    }
    super = {
        "abstract": "super",
        "id": "super1",
        "flags": ["flags1", "flags2"],
        "num": 10,
        "num1": 100
    }
    result = process_json_inheritance(sub, super)

    assert result == {'id': 'sub', 'flags': [
        'flags2', 'flags3'], 'num': 20, 'num1': 20.0, 'looks_like': 'super1', 'type': 'one'}


if __name__ == "__main__":
    test()
