import os
import json
import copy
from .mod import mod


def __scan_mods(path: str) -> list[mod]:
    path = os.path.expanduser(path)
    mods: list[mod] = []
    files = os.listdir(path)
    for file in files:
        file = os.path.join(path, file)
        if os.path.isdir(file):
            mods += __scan_mods(file)
        else:
            mods += __scan_modinfo(file)
    return mods


def __scan_modinfo(file: str) -> list[mod]:
    mods: list[mod] = []
    if (file.endswith("modinfo.json")):
        with open(file, encoding="utf-8") as fp:
            jsondata = json.load(fp)
        if type(jsondata) is list:
            for jsondata_item in jsondata:
                if jsondata_item["type"] == "MOD_INFO":
                    mods.append(mod(jsondata_item, os.path.dirname(file)))
        elif type(jsondata) is dict:
            mods.append(mod(jsondata, os.path.dirname(file)))
    return mods


def find_mod(mods: list[mod], id: str) -> mod:
    for mod in mods:
        if id == mod.id:
            return mod


def __sort_mods(mods: list[mod]) -> list[mod]:
    result: list[mod] = []
    my_mods: list[mod] = copy.deepcopy(mods)
    while len(my_mods) > 0:
        for my_mod in my_mods[::-1]:
            if len(my_mod.dependencies) == 0:
                result.append(find_mod(mods, my_mod.id))
                my_mods.remove(my_mod)
            # remove no have dependen mod
            for dependen in my_mod.dependencies:
                hasFlag = False
                for mod in mods:
                    if dependen == mod.id:
                        hasFlag = True
                        break
                if not hasFlag:
                    my_mods.remove(my_mod)
        for my_mod in my_mods:
            for dependen in my_mod.dependencies[::-1]:
                for result_mod in result:
                    if dependen == result_mod.id:
                        my_mod.dependencies.remove(dependen)
    return result


def get_sort_mods(path: str) -> list[mod]:
    return __sort_mods(__scan_mods(path))


if __name__ == "__main__":
    for my_mod in get_sort_mods("~/Downloads/Cataclysm-DDA-master/data/mods/"):
        print(my_mod)
