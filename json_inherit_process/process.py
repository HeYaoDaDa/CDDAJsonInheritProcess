import os
import json

from .process_helper import process_json_inheritance, add_json_to_processed_json_list_dict, get_json_id_str, dump_json, get_json_type_str, equal_id


class processer:

    def __init__(self, processed_json_list_dict: dict, wait_process_json_list_dict: dict, wait_process_json_file_dict: dict) -> None:
        self.processed_json_list_dict = processed_json_list_dict
        self.wait_process_json_list_dict = wait_process_json_list_dict
        self.wait_process_json_file_dict = wait_process_json_file_dict
        self.count_id = 0

    def add_processed_json_list_dict(self, json_object: dict):
        add_json_to_processed_json_list_dict(
            json_object, self.processed_json_list_dict)
        self.process_wait_json_object(json_object)

    def add_wait_process_json_file_dict(self, json_objects: list, wait_ids: list, out_file: str):
        item = {
            "wait_ids": wait_ids,
            "json_objects": json_objects
        }
        self.wait_process_json_file_dict[out_file] = item

    def process_wait_file(self, process_json_object: dict, wait_id: int, wait_file: str):
        wait_process_json_file_item = self.wait_process_json_file_dict[wait_file]
        wait_ids = wait_process_json_file_item["wait_ids"]
        wait_json_objects = wait_process_json_file_item["json_objects"]
        for index in range(len(wait_ids))[::-1]:
            file_wait_id = wait_ids[index]
            if wait_id == file_wait_id:
                del wait_ids[index]
        for index, json_object in enumerate(wait_json_objects):
            if json_object == wait_id:
                wait_json_objects[index] = process_json_object
        if len(wait_ids) == 0:
            dump_json(wait_json_objects, wait_file)
            del self.wait_process_json_file_dict[wait_file]

    def process_wait_json_object(self, new_processed_json_object: dict):
        new_processed_json_object_id = get_json_id_str(
            new_processed_json_object)
        new_processed_json_object_type = get_json_type_str(
            new_processed_json_object)
        if new_processed_json_object_type in self.wait_process_json_list_dict.keys():
            for index in range(len(self.wait_process_json_list_dict[new_processed_json_object_type]))[::-1]:
                wait_process_json_object = self.wait_process_json_list_dict[
                    new_processed_json_object_type][index]
                if equal_id(wait_process_json_object["copy-from"], new_processed_json_object_id):
                    wait_id = wait_process_json_object["wait_id"]
                    wait_file = wait_process_json_object["wait_file"]
                    del wait_process_json_object["wait_id"]
                    del wait_process_json_object["wait_file"]
                    processed_json_object = process_json_inheritance(
                        wait_process_json_object, new_processed_json_object)
                    del self.wait_process_json_list_dict[new_processed_json_object_type][index]
                    self.add_processed_json_list_dict(processed_json_object)
                    self.process_wait_file(
                        processed_json_object, wait_id, wait_file)

    def process_json_inheritance_file(self, json_file: str, out_file: str):
        with open(json_file, encoding="utf-8") as fp:
            json_data = json.load(fp)
        try:
            json_objects = json_data if type(
                json_data) is list else [json_data]
            my_file_processer = file_processer(self, json_objects)
            my_file_processer.process()
            for processed_json_object in my_file_processer.current_processed_json_object_list:
                self.add_processed_json_list_dict(processed_json_object)
            if len(my_file_processer.current_wait_super_json_object_list) == 0:
                dump_json(json_objects, out_file)
            else:
                wait_ids = []
                for wait_json_object in my_file_processer.current_wait_super_json_object_list:
                    wait_ids.append(wait_json_object["wait_id"])
                    wait_json_object["wait_file"] = out_file
                    add_json_to_processed_json_list_dict(
                        wait_json_object, self.wait_process_json_list_dict)
                self.add_wait_process_json_file_dict(
                    json_objects, wait_ids, out_file)
        except Exception as E:
            print("Error in JSON file: '{0}'".format(json_file))
            raise E

    def process_json_inheritance_dir(self, dir_path: str,  out_path: str):
        allfiles = sorted(os.listdir(dir_path))
        dirs = []
        for file in allfiles:
            full_json_file = os.path.join(dir_path, file)
            full_out_file = os.path.join(out_path, file)
            if os.path.isdir(full_json_file):
                dirs.append((full_json_file, full_out_file))
            elif file.endswith(".json"):
                self.process_json_inheritance_file(
                    full_json_file, full_out_file)
            else:
                print("Skipping file: '{}'".format(file))
        for json_dir, out_dir in dirs:
            self.process_json_inheritance_dir(json_dir, out_dir)


class file_processer:
    def __init__(self, external_obj: processer, wait_process_json_object_list: list) -> None:
        self.external_obj = external_obj
        self.processed_json_object_map = external_obj.processed_json_list_dict
        self.wait_process_json_object_list = wait_process_json_object_list if type(
            wait_process_json_object_list) is list else [wait_process_json_object_list]
        self.current_processed_json_object_list = []
        self.current_wait_super_json_object_list = []

    def add_processed_json_list_dict(self, json_object: dict, wait_id: int = None):
        self.current_processed_json_object_list.append(json_object)
        if wait_id != None:
            for index, current_processed_json_object in enumerate(self.wait_process_json_object_list):
                if current_processed_json_object == wait_id:
                    self.wait_process_json_object_list[index] = json_object
        self.process_wait_json_object(json_object)

    def add_wait_process_json_object_list(self, json_object: dict) -> int:
        json_object["wait_id"] = self.external_obj.count_id
        self.current_wait_super_json_object_list.append(json_object)
        self.external_obj.count_id += 1
        return json_object["wait_id"]

    def process_wait_json_object(self, json_object: dict):
        new_processed_json_object_id = get_json_id_str(
            json_object)
        new_processed_json_object_type = get_json_type_str(
            json_object)
        if new_processed_json_object_id == None or new_processed_json_object_type == None:
            return
        processed_json_object_list = []
        for index in range(len(self.current_wait_super_json_object_list))[::-1]:
            current_wait_super_json_object = self.current_wait_super_json_object_list[index]
            if new_processed_json_object_type == get_json_type_str(current_wait_super_json_object) and equal_id(current_wait_super_json_object["copy-from"], new_processed_json_object_id):
                wait_id = current_wait_super_json_object["wait_id"]
                del current_wait_super_json_object["wait_id"]
                processed_json_object = process_json_inheritance(
                    current_wait_super_json_object, json_object)
                del self.current_wait_super_json_object_list[index]
                # TODO
                # self.add_processed_json_list_dict(processed_json_object)
                processed_json_object_list.append(
                    (processed_json_object, wait_id))
        for item in processed_json_object_list:
            self.add_processed_json_list_dict(item)

    def process_json_inheritance_object(self, json_object: dict) -> dict:
        if "copy-from" not in json_object:
            self.add_processed_json_list_dict(json_object)
            return json_object
        else:
            super_json_object = self.find_super_json(json_object)
            if (super_json_object == None):
                return self.add_wait_process_json_object_list(json_object)
            else:
                processed_json_object = process_json_inheritance(
                    json_object, super_json_object)
                self.add_processed_json_list_dict(
                    processed_json_object)
                return processed_json_object

    def find_super_json(self, json_object: dict):
        super_id = json_object["copy-from"]
        json_type = get_json_type_str(json_object)
        for current_json_object in self.current_processed_json_object_list[::-1]:
            if json_type == get_json_type_str(current_json_object) and equal_id(super_id, get_json_id_str(current_json_object)):
                return current_json_object
        if json_type in self.processed_json_object_map.keys():
            for processed_json_object in self.processed_json_object_map[json_type][::-1]:
                if equal_id(super_id, get_json_id_str(processed_json_object)):
                    return processed_json_object

    def process(self):
        self.wait_process_json_object_list = self.wait_process_json_object_list if type(
            self.wait_process_json_object_list) is list else [self.wait_process_json_object_list]
        for index, json_object in enumerate(self.wait_process_json_object_list):
            self.wait_process_json_object_list[index] = self.process_json_inheritance_object(
                json_object)
