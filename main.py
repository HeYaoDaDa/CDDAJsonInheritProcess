#!/usr/bin/env python3

import os
import shutil
from argparse import ArgumentParser
from json_inherit_process.process import processer
from json_inherit_process.process_helper import get_json_id_str

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

print("Start process.\ndata_dir is {}\nout_dir is {}."
      .format(args.data_dir, args.out_dir))
my_processer = processer({}, {}, {})
my_processer.process_json_inheritance_dir(args.data_dir[0], args.out_dir)
print(len(my_processer.wait_process_json_file_dict.keys()))
for k, v in my_processer.wait_process_json_file_dict.items():
    print("{}:{}".format(k, v["wait_ids"]))
    # for i in v["json_objects"]:
    #     print(i)
