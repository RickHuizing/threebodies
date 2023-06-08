import os
import re
import shutil

import numpy as np


def create_folder(name, path):
    os.makedirs(f"{path}/{name}", exist_ok=True)


def organize_data(config_name, delete_old_files=False):
    # paths to input and output folders
    input_path = f"./results/{config_name}"
    output_path = f"./results/pre-processed/{config_name}"

    file_types = {"plots": ".png", "text_data": ".txt", "numpy_data": ".npy"}

    # create output folders
    for file_type, _ in file_types.items():
        create_folder(file_type, output_path)

    # gather all files and put them in folders by file type
    for root, dirs, files in os.walk(input_path):
        iteration_name: str = root.split("/")[-1]
        for file_type, extension in file_types.items():
            for file in files:
                if file.endswith(extension):
                    input_file = root + "/" + file
                    output_file = f"{output_path}/{file_type}/{iteration_name}-{file}"
                    if delete_old_files:
                        shutil.move(input_file, output_file)
                    else:
                        shutil.copyfile(input_file, output_file)


def merge_numpy_data(config_name, limit=1, complete=False):
    input_path = f"./results/pre-processed/{config_name}/numpy_data"
    files = os.listdir(input_path)
    files.sort()
    if complete:
        files = filter(lambda file: file.startswith('_'), files)
    else:
        files = filter(lambda file: not file.startswith('_'), files)

    # gather leading numbers
    if complete:
        datasets = {re.search(r"^\d+", filename).group() for filename in files}
    else:
        datasets = {re.search(r"^_\d+", filename).group() for filename in files}

    for dataset in list(datasets)[:limit]:
        x, y = np.load(f"{input_path}/{dataset}-xy_npy.npy")
        vx, vy = np.load(f"{input_path}/{dataset}-vxvy_npy.npy")

        merged_set = np.array([x, y, vx, vy])
        np.save



if __name__ == "__main__":
    organize_data("breen-et-al-00001-es2")

