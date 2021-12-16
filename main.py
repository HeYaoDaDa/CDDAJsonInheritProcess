#!/usr/bin/env python3

import copy
import os
import shutil
from argparse import ArgumentParser
from json_inherit_process.mod import mod
from json_inherit_process.process import processer
from json_inherit_process.process_helper import get_json_id_str
from json_inherit_process.mod_helper import get_sort_mods, find_mod

parser = ArgumentParser("CDDA json inherit processer", "Process CDDA json inherit",
                        description="specify game data path, output path")
parser.add_argument("-d", "--data_dir", dest="data_dir",
                    help="game data/ path", type=str, nargs="*")
parser.add_argument("-o", "--out_dir", dest="out_dir",
                    help="translated json file output path", type=str)
args = parser.parse_args()

if not args.data_dir:
    print("Have to specify game data/ path")
    exit(1)
for data_dir in args.data_dir:
    if not os.path.exists(data_dir):
        print("{} is not exist".format(data_dir))
        exit(1)
    elif not os.path.isdir(data_dir):
        print("{} is not dir".format(data_dir))
        exit(1)

if not args.out_dir:
    print("Have to specify translated json file output path")
    exit(1)


if os.path.exists(args.out_dir):
    shutil.rmtree(args.out_dir, True)
os.mkdir(args.out_dir)

ex_paths = ["~/Downloads/Cataclysm-DDA-master/data/mods"]

for index, path in enumerate(ex_paths):
    ex_paths[index] = os.path.expanduser(path)


def process_mod(dir_paths: list, exclude_paths: list, out_dir: str):
    my_processer = processer({}, {}, {})
    for dir_path in dir_paths:
        my_processer.process_json_inheritance_dir(
            dir_path, exclude_paths, out_dir)
    my_processer.clear_wait_file()
    print(len(my_processer.wait_process_json_file_dict.keys()))
    for k, v in my_processer.wait_process_json_file_dict.items():
        print("{}:{}".format(k, v["wait_ids"]))
    for k, v in my_processer.wait_process_json_list_dict.items():
        print(k)
        for i in v:
            print(
                "\tcopyt-from is {}, id is {},\n\t\t {}".format(i["copy-from"], get_json_id_str(i), i))
    return my_processer.processed_json_list_dict


def process_mod(my_mod: mod, dependent_json_object_map: dict, exclude_paths: list[str], out_dir: str):
    my_processer = processer(dependent_json_object_map, {}, {})
    for dir_path in my_mod.path:
        my_processer.process_json_inheritance_dir(
            dir_path, exclude_paths, out_dir)
    my_processer.clear_wait_file()
    print(len(my_processer.wait_process_json_file_dict.keys()))
    for k, v in my_processer.wait_process_json_file_dict.items():
        print("{}:{}".format(k, v["wait_ids"]))
    for k, v in my_processer.wait_process_json_list_dict.items():
        print(k)
        for i in v:
            print(
                "\tcopyt-from is {}, id is {},\n\t\t {}".format(i["copy-from"], get_json_id_str(i), i))
    return my_processer.current_mod_process_json_map


def add_json_object_map(one: dict, two: dict) -> dict:
    result = copy.deepcopy(two)
    for one_key, one_value in one.items():
        if one_key in two:
            result[one_key] += one_value
        else:
            result[one_key] = one_value
    return result


def process_game(game_data: str, out_dir: str):
    mods: list[mod] = get_sort_mods(game_data)
    for my_mod in mods:
        exclude_paths: list[str] = []
        if my_mod.id == "dda":
            my_mod.path.append(game_data)
            exclude_paths.append(os.path.join(game_data, "mods"))
        print(my_mod)
        print(exclude_paths)
        dependent_json_object_map = {}
        for dependent_id in my_mod.dependencies:
            dependent_mod = find_mod(mods, dependent_id)
            dependent_json_object_map = add_json_object_map(
                dependent_json_object_map, dependent_mod.processed_json_object_map)
        my_mod.processed_json_object_map = process_mod(
            my_mod, dependent_json_object_map, exclude_paths, os.path.join(out_dir, my_mod.id))


print("Start process.\ndata_dir is {}\nout_dir is {}."
      .format(args.data_dir, args.out_dir))
process_game(args.data_dir[0], args.out_dir)
