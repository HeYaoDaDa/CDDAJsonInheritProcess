#!/usr/bin/env python3
" Procees CDDA Json inherit "

import json
import os
from optparse import OptionParser
import copy

parser = OptionParser()
parser.add_option("-v", "--verbose", dest="verbose", help="be verbose")
parser.add_option("-o", "--out", dest="out_dir",default="../processed/",help="out dir")
parser.add_option("-t", "--target", dest="target_dir",default=".",help="target dir")
(options, args) = parser.parse_args()

def init_out_dir():
    if not os.path.exists(options.out_dir):
            os.makedirs(options.out_dir)
            if(options.verbose):
                print("mkdir out_dir {}".format(options.out_dir))

def scan_mods(path:str):
    mods = []
    files = join_files(os.listdir(path),path)
    for file in files:
        if os.path.isdir(file):
            mods += scan_mods(file)
        else:
            mods += scan_modinfo(file)
    return mods

def join_files(files:list,dir:str):
    result = []
    for file in files:
        result.append(os.path.join(dir,file))
    return result

def scan_modinfo(file:str):
    mods = []
    if (file.endswith("modinfo.json")):
        with open(file, encoding="utf-8") as fp:
            jsondata = json.load(fp)
        if type(jsondata) is list:
            for jsondata_item in jsondata:
                if jsondata_item["type"] == "MOD_INFO":
                    mods.append(convert_my_mod_dict(jsondata_item, os.path.dirname(file)))
        elif type(jsondata) is dict:
            mods.append(convert_my_mod_dict(jsondata, os.path.dirname(file)))
        elif options.verbose:
            print("ignore json type {}".format(jsondata))
    return mods

def sort_mods(mods:list):
    result = []
    my_mods = copy.deepcopy(mods)
    while len(my_mods) > 0:
        for mod in my_mods[::-1]:
            if "dependencies" not in mod or len(mod["dependencies"]) == 0:
                result.append(find_mod(mods,mod["id"]))
                my_mods.remove(mod)
        for mod in my_mods:
            for dependen in mod["dependencies"][::-1]:
                for result_mod in result:
                    if dependen == result_mod["id"]:
                        mod["dependencies"].remove(dependen)
    return result

def convert_my_mod_dict(jsondata:dict,path:str):
    result = {}
    result["id"] = jsondata["id"]
    result["name"] = jsondata["name"]
    if result["id"] == "dda":
        result["path"] = options.target_dir
    else:
        result["path"] = path
    if "dependencies" in jsondata:
        result["dependencies"] = jsondata["dependencies"]
    else:
        result["dependencies"] = []
    return result

        
def find_mod(mods:list,id:str):
    for mod in mods:
        if id == mod["id"]:
            return mod

def scan_all_json(path:str):
    jsons = []
    files = join_files(os.listdir(path),path)
    for file in files:
        if os.path.isdir(file) and not file.endswith("mods"):
            jsons += scan_all_json(file)
        else:
            jsons += scan_json(file)
    return jsons

def scan_json(file:str):
    jsons = []
    if (file.endswith(".json")):
        with open(file, encoding="utf-8") as fp:
            jsondata = json.load(fp)
        if type(jsondata) is list:
            for jsondata_item in jsondata:
                jsons.append(jsondata_item)
        elif type(jsondata) is dict:
            jsons.append(jsondata)
        elif options.verbose:
            print("ignore json type {}".format(jsondata))
    return jsons

def process_json_dir(path:str,jsons:list,process_jsons:list):
    files = os.listdir(path)
    for file in files:
        out_file = os.path.join(options.out_dir,path,file)
        file = os.path.join(path,file)
        if os.path.isdir(file) and not file.endswith("mods"):
            process_json_dir(file,jsons,process_jsons)
        else:
            process_json_file(file,out_file,jsons,process_jsons)

def process_json_file(file:str,out_file:str,jsons:list,process_jsons:list):
    if (file.endswith(".json")):
        with open(file, encoding="utf-8") as fp:
            file_json_data = json.load(fp)
        file_json_data = convert_jsons(file_json_data)
        if type(file_json_data) is list:
            for jsondata_item in file_json_data:
                process_json(jsondata_item,jsons,process_jsons)
        elif type(file_json_data) is dict:
            process_json(file_json_data,jsons,process_jsons)
        elif options.verbose:
            print("ignore json type {}".format(file_json_data))
        if not os.path.exists(os.path.dirname(out_file)):
            os.makedirs(os.path.dirname(out_file))
        json.dump(file_json_data, open(out_file, mode="w", encoding="utf-8"), ensure_ascii=False, indent=2)

def process_json_unit(jsondata:dict,jsons:list,process_jsons:list):
    if("copy-from" in jsondata):
        super_json = find_json(jsondata,process_jsons)
        if super_json == None:
            super_json = find_json(jsondata,jsons)
        if super_json != None and "copy-from" in super_json:
            process_json_unit(super_json,jsons,processed_jsons)
        process_json_data = process_json_inheritance(jsondata,super_json)
        jsondata.clear()
        jsondata.update(process_json_data)

def process_json(jsondata:dict,jsons:list,process_jsons:list):
    process_json_unit(jsondata,jsons,process_jsons)
    processed_jsons.append(jsondata)

def get_id(jsondata:dict):
    result = None
    if "id" in jsondata:
        result = jsondata["id"]
    elif "result" in jsondata:
        if "id_suffix" in jsondata:
            result = jsondata["result"] + "_" + jsondata["id_suffix"]
        else:
            result = jsondata["result"]
    elif "abstract" in jsondata:
        result = jsondata["abstract"]
    return result

def find_json(jsondata:dict,jsons:list):
    type_groups = [
        ["recipe","practice"],
        ["GENERIC","AMMO","MAGAZINE","ARMOR","TOOL","PET_ARMOR","BOOK","BIONIC_ITEM","COMESTIBLE","GUN","GUNMOD","BATTERY"]
    ]
    result = None
    id = jsondata["copy-from"]
    type = jsondata["type"]
    eq_id_jsons = []
    eq_id_type_group = []
    eq_id_type_jsons = []
    this_type_group = []
    for type_group in type_groups:
        if type in type_group:
            this_type_group = type_group
            break
    for i in jsons:
        if "type" in i:
            if "copy-from" in i and i["copy-from"] == get_id(i):
                continue
            if id == get_id(i):
                eq_id_jsons.append(i)
    for i in eq_id_jsons:
        if "type" in i:
            if type == i["type"]:
                eq_id_type_jsons.append(i)
            if i["type"] in this_type_group:
                eq_id_type_group.append(i)
            
    if len(eq_id_type_jsons) == 1:
        result = eq_id_type_jsons[0]
    elif len(eq_id_type_group) == 1:
        result = eq_id_type_group[0]

    return result

def process_json_inheritance(sub:dict, super:dict):
    # print()
    if super == None:
        print("WARR no super,copy-from is {},type is {}".format(sub["copy-from"],sub["type"]))
        result = {}
    else:
        result = copy.deepcopy(super)
    #TODO looks_like
    my_sub = copy.deepcopy(sub)
    del my_sub["copy-from"]
    if "abstract" in result:
        del result["abstract"]
    if "relative" in my_sub:
        result = process_relative(my_sub["relative"],result)
        del my_sub["relative"]
    
    if "proportional" in my_sub:
        result = process_proportional(my_sub["proportional"],result)
        del my_sub["proportional"]

    if "extend" in my_sub:
        for key,value in my_sub["extend"].items():
            if key in result:
                if not type(value) is list:
                    value = [value]
                if not type(result[key]) is list:
                    result[key] = [result[key]]
                result[key] += value
            else:
                result[key] = value
        del my_sub["extend"]

    if "delete" in my_sub:
        for key,value in my_sub["delete"].items():
            if key in result:
                if not type(value) is list:
                    value = [value]
                if not type(result[key]) is list:
                    result[key] = [result[key]]
                for i in result[key]:
                    if i in value:
                        del i
        del my_sub["delete"]

    for key,value in my_sub.items():
        result[key] = value
    
    return result

def process_proportional(sub:dict,super:dict):
    my_sub = copy.deepcopy(sub)
    result = copy.deepcopy(super)
    for key,value in my_sub.items():
        if key in result:
            if type(result[key]) is str:
                if have_int(result[key]):
                    num,suf = get_int(result[key])
                    result[key] = str(num*value) + " " + suf
            elif type(result[key]) is dict:
                result[key] = process_proportional(value, result[key])
            else:
                result[key] *= value
        else:
            if options.verbose:
                print("--------Warring : proportional")
    return result

def process_relative(sub:dict,super:dict):
    my_sub = copy.deepcopy(sub)
    result = copy.deepcopy(super)
    for key,value in my_sub.items():
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
                        num,suf = get_int(result[key])
                    else:
                        num = result[key]
                    if type(value) is str:
                        num1,suf1 = get_int(result[key])
                    else:
                        num1 = value
                    if suf == "":
                        suf = suf1
                    if suf1 == "":
                        suf1 = suf
                    if suf != suf1:
                        print("suf:{}  suf1:{}".format(suf,suf1))
                    result[key] = str(num + num1) + " " + suf
            else:
                result[key] += value
        else:
            result[key] = value
    return result
def get_int(s:str):
    d = ["0","1","2","3","4","5","6","7","8","9"]
    index = -1
    for i in range(len(s))[::-1]:
        if not s[i] in d:
            index = i
    return float(s[:index]),s[index:].lstrip()

def have_int(s:str):
    d = ["0","1","2","3","4","5","6","7","8","9"]
    for i in range(len(s))[::-1]:
        if s[i] in d:
            return True
    return False

def convert_jsons(jsons:list):
    result = []
    if type(jsons) is dict:
        return convert_json(jsons)
    for json_data in jsons:
        result += convert_json(json_data)
    return result

def convert_json(json_data:dict):
    result = []
    if "id" in json_data and type(json_data["id"]) is list:
        for id in json_data["id"]:
            json_data_sub = copy.deepcopy(json_data)
            json_data_sub["id"] = id
            result.append(json_data_sub)
    else:
        result.append(json_data)
    return result
mods = sort_mods(scan_mods(options.target_dir))
init_out_dir()
old_jsons = []
processed_jsons = []
for mod in mods:
    print("==> {} <==".format(mod["name"]))
    old_jsons = convert_jsons(scan_all_json(mod["path"]))
    process_json_dir(mod["path"],old_jsons,processed_jsons)
# print(find_json({"copy-from":"generic_city_building_no_sidewalk","type":"overmap_terrain"},old_jsons))
