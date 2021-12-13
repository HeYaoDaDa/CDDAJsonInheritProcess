import copy


def process_json_inheritance(sub_json_object: dict, super_json_object: dict):
    # print()
    if super_json_object == None:
        print(
            "WARR no super,copy-from is {},type is {}".format(sub_json_object["copy-from"], sub_json_object["type"]))
        processed_json_object = {}
    else:
        processed_json_object = copy.deepcopy(super_json_object)

    # sub json have look like super
    if "id" in processed_json_object:
        processed_json_object["looks_like"] = processed_json_object["id"]

    if "abstract" in processed_json_object:
        del processed_json_object["abstract"]

    inherit_templet = copy.deepcopy(sub_json_object)

    del inherit_templet["copy-from"]

    if "relative" in inherit_templet:
        processed_json_object = process_relative(
            inherit_templet["relative"], processed_json_object)
        del inherit_templet["relative"]

    if "proportional" in inherit_templet:
        processed_json_object = process_proportional(
            inherit_templet["proportional"], processed_json_object)
        del inherit_templet["proportional"]

    if "extend" in inherit_templet:
        for key, value in inherit_templet["extend"].items():
            if key in processed_json_object:
                if not type(value) is list:
                    value = [value]
                if not type(processed_json_object[key]) is list:
                    processed_json_object[key] = [processed_json_object[key]]
                processed_json_object[key] += value
            else:
                processed_json_object[key] = value
        del inherit_templet["extend"]

    if "delete" in inherit_templet:
        for key, value in inherit_templet["delete"].items():
            if key in processed_json_object:
                if not type(value) is list:
                    value = [value]
                if not type(processed_json_object[key]) is list:
                    processed_json_object[key] = [processed_json_object[key]]
                for i in processed_json_object[key]:
                    if i in value:
                        del i
        del inherit_templet["delete"]

    for key, value in inherit_templet.items():
        processed_json_object[key] = value

    return processed_json_object


def process_proportional(sub: dict, super: dict):
    my_sub = copy.deepcopy(sub)
    result = copy.deepcopy(super)
    for key, value in my_sub.items():
        if key in result:
            if type(result[key]) is str:
                if have_int(result[key]):
                    num, suf = get_int(result[key])
                    result[key] = str(num*value) + " " + suf
            elif type(result[key]) is dict:
                result[key] = process_proportional(value, result[key])
            else:
                result[key] *= value
    return result


def process_relative(sub: dict, super: dict):
    my_sub = copy.deepcopy(sub)
    result = copy.deepcopy(super)
    for key, value in my_sub.items():
        if key in result:
            if type(result[key]) is dict:
                result[key] = process_relative(value, result[key])
            elif type(result[key]) is str or type(value) is str:
                if (type(result[key]) is str and have_int(result[key])) or (type(value) is str and have_int(value)):
                    num = 0
                    num1 = 0
                    suf = ""
                    suf1 = ""
                    if type(result[key]) is str:
                        num, suf = get_int(result[key])
                    else:
                        num = result[key]
                    if type(value) is str:
                        num1, suf1 = get_int(result[key])
                    else:
                        num1 = value
                    if suf == "":
                        suf = suf1
                    if suf1 == "":
                        suf1 = suf
                    if suf != suf1:
                        print("suf:{}  suf1:{}".format(suf, suf1))
                    result[key] = str(num + num1) + " " + suf
            else:
                result[key] += value
        else:
            result[key] = value
    return result


def get_int(s: str):
    d = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    index = -1
    for i in range(len(s))[::-1]:
        if not s[i] in d:
            index = i
    return float(s[:index]), s[index:].lstrip()


def have_int(s: str):
    d = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(len(s))[::-1]:
        if s[i] in d:
            return True
    return False
