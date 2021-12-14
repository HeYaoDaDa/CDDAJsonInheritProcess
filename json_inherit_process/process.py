import copy
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
