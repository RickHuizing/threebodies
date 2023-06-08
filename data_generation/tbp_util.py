import os

import numpy as np

# name of the configuration used to generate the data
config_name = "breen-et-al-00001"

# path to data
input_path = f"./results/{config_name}"


def load_dataset(dataset_name):
    data = np.load(f"{input_path}/{dataset_name}/data.npz")

    x, y, vx, vy = [data[x] for x in data]
    return x, y, vx, vy


def load_datasets(load_successful=True, load_unsuccessful=False, limit=1):
    datasets = os.scandir(input_path)
    datasets = filter(lambda file: file.is_dir(), datasets)
    datasets = [ds.name for ds in datasets]

    if load_successful and not load_unsuccessful:
        datasets = filter(lambda name: not name.startswith("_"), datasets)
    elif load_unsuccessful and not load_successful:
        datasets = filter(lambda name: name.startswith("_"), datasets)

    for dataset in list(datasets)[:limit]:
        x, y, vx, vy = load_dataset(dataset)
        yield dataset, x, y, vx, vy
