import os


def save_to_disk(content, path):
    dir = os.path.dirname(path)
    os.makedirs(dir, exist_ok=True)
    with open(path, "w") as file:
        file.write(content)


def open_runs(path):
    keys = ("run_number", "reconstruction")
    with open(path, "r") as file:
        return [dict(zip(keys, line.strip().split(" "))) for line in file]
