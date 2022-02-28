import copy
import os
import shutil
from .mod import mod
from .process import processer
from .process_helper import get_json_id_str
from .mod_helper import get_sort_mods, find_mod


def process_mod(my_mod: mod, dependent_json_object_map: dict, exclude_paths: list[str], out_dir: str):
    my_processer = processer(dependent_json_object_map, {}, {})
    for dir_path in my_mod.path:
        my_processer.process_json_inheritance_dir(
            dir_path,
            exclude_paths,
            out_dir
        )
    my_processer.clear_wait_file()
    print(
        f"wait process json file dict have :{len(my_processer.wait_process_json_file_dict.keys())}")
    for k, v in my_processer.wait_process_json_file_dict.items():
        print("{}:{}".format(k, v["wait_ids"]))
    for k, v in my_processer.wait_process_json_list_dict.items():
        print(k)
        for i in v:
            print(
                "\tcopyt-from is {}, id is {},\n\t\t json is :{}"
                .format(
                    i["copy-from"], get_json_id_str(i), i
                )
            )
    return my_processer.current_mod_process_json_map


def add_json_object_map(one: dict, two: dict) -> dict:
    result = copy.deepcopy(two)
    for one_key, one_value in one.items():
        if one_key in two:
            result[one_key] += one_value
        else:
            result[one_key] = one_value
    return result


def process_game(game_data: str, out_dir: str, is_old_game: bool = False):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, True)
    os.mkdir(out_dir)
    mods: list[mod] = get_sort_mods(game_data)
    for my_mod in mods:
        exclude_paths: list[str] = []
        if is_old_game and my_mod.id == "dda":
            my_mod.path.append(game_data)
            exclude_paths.append(os.path.join(game_data, "mods"))
        print(f"----- {my_mod.name}({my_mod.id}) -----")
        print(f"exclude paths is {exclude_paths}")
        dependent_json_object_map = {}
        for dependent_id in my_mod.dependencies:
            dependent_mod = find_mod(mods, dependent_id)
            dependent_json_object_map = add_json_object_map(
                dependent_json_object_map, dependent_mod.processed_json_object_map)
        my_mod.processed_json_object_map = process_mod(
            my_mod, dependent_json_object_map, exclude_paths, os.path.join(out_dir, my_mod.id))
