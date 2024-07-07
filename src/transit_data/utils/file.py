import os
import json


def write_dict_to_file(dictionary: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w") as json_file:
        json.dump(dictionary, json_file, indent=4)
