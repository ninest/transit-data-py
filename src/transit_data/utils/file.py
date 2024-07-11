import os
import json
import requests
import zipfile


def write_dict_to_file(dictionary: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as json_file:
        json.dump(dictionary, json_file, indent=4)


def download_zip(url, save_path):
    # Ensure the save_path directory exists
    os.makedirs(save_path, exist_ok=True)

    response = requests.get(url)
    zip_path = os.path.join(save_path, "downloaded.zip")

    # Save the zip file to the specified path
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(save_path)

    # Remove the zip file after extraction
    os.remove(zip_path)
