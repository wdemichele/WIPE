import json
import os
from typing import List

ROOT_DIR = ROOT_DIR = r"C:\Projects\Research\SWEEP\SWEEP"


def open_file(file_path, file_type=".txt"):
    """Open file."""
    if file_type == ".txt":
        with open(file_path, "r") as f:
            file_content = f.read()
    elif file_type == ".json":
        with open(file_path, "r") as f:
            file_content = json.load(f)
    elif not file_type:
        if file_path.endswith(".txt"):
            open_file(file_path, ".txt")
        elif file_path.endswith(".json"):
            open_file(file_path, ".json")
        else:
            raise ValueError("File type not specified.")
    else:
        raise ValueError(f"File type {file_type} not supported.")
    return file_content

def get_sectors(train=True) -> List[str]:
    data_path = os.path.join(ROOT_DIR, "data", f'{"train" if train else "test"}')
    return [sector for sector in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, sector))]

def get_activities(sector: str, train=True) -> List[str]:
    sector_path = os.path.join(ROOT_DIR, "data", f'{"train" if train else "test"}', sector)
    return [activity for activity in os.listdir(sector_path) if os.path.isdir(os.path.join(sector_path, activity))]
