import copy

from json_inherit_process.helper import test1
from .processer.extend import process_extend
from .processer.delete import process_delete
from .processer.proportional import process_proportional
from .processer.relative import process_relative


def process_json_inheritance(sub_json_object: dict, super_json_object: dict):
    if super_json_object == None:
        print(
            "WARR no super,copy-from is {},type is {}".format(sub_json_object["copy-from"], sub_json_object["type"]))
        processed_json_object = {}
    else:
        processed_json_object = copy.deepcopy(super_json_object)

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

    if "abstract" in processed_json_object:
        del processed_json_object["abstract"]

    return processed_json_object


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
