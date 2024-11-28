import airfrans as af
import os
from pathlib import Path
from typing import Tuple
# This has already been run
# Download the dataset
# NOTE: Dataset documentation can be found here: https://airfrans.readthedocs.io/en/latest/notes/dataset.html

def download_airfrans_data(directory_name: Path, file_name: str, task: str, dataset_type: str) -> Tuple[list, list]:
  if not directory_name.exists() or not any(directory_name.iterdir()):
    af.dataset.download(root=str(directory_name), file_name=file_name, unzip=True, OpenFOAM=False)
  dataset_list, dataset_name = af.dataset.load(root=str(directory_name/file_name), task = task, train = dataset_type)
  return dataset_list, dataset_name