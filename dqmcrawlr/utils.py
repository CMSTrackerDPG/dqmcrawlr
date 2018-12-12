import os


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
