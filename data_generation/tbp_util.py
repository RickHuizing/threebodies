import os

import numpy as np


class GlobalConfig:
    pass


__global_config = GlobalConfig()
# name of the configuration used to generate the data
__global_config.config_name = "verlet-000001"


# I know, I know, but I don't wanna pollute the parameters too much
def use_config(name: str):
    print(f"Setting {name} as the configuration to load trajectories from")
    __global_config.config_name = name


# path to data
def get_input_path():
    return f"./results/{__global_config.config_name}"


def load_dataset(dataset_name):
    data = np.load(f"{get_input_path()}/{dataset_name}/data.npz")

    x, y, vx, vy = [data[x] for x in data]
    return x, y, vx, vy


def load_datasets(load_successful=True, load_unsuccessful=False, limit=1):
    datasets = os.scandir(get_input_path())
    datasets = filter(lambda file: file.is_dir(), datasets)
    datasets = [ds.name for ds in datasets]
    datasets = sorted(datasets)

    if load_successful and not load_unsuccessful:
        datasets = filter(lambda name: not name.startswith("_"), datasets)
    elif load_unsuccessful and not load_successful:
        datasets = filter(lambda name: name.startswith("_"), datasets)

    for dataset in list(datasets)[:limit]:
        x, y, vx, vy = load_dataset(dataset)
        yield dataset, x, y, vx, vy
    print(f"loaded {len(list(datasets))} datasets")
