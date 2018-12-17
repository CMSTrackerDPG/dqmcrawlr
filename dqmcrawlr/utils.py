import json
import os

DATASET_CACHE_FILE_NAME = ".dqmcrawlrcache.json"


def save_to_disk(content, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w") as file:
        file.write(content)


def open_runs(path):
    keys = ("run_number", "reconstruction")
    with open(path, "r") as file:
        return [dict(zip(keys, line.strip().split(" "))) for line in file]


def open_dataset_cache():
    try:
        with open(DATASET_CACHE_FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def save_dataset_cache_to_disk(cache):
    with open(DATASET_CACHE_FILE_NAME, "w") as file:
        file.write(json.dumps(cache))
