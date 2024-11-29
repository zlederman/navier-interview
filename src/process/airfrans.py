from pathlib import Path
import os
from src.process.vtk_xml import extract_from_vtk, extract_num_points_from_xml
from typing import List
import h5py
from xml.etree.ElementTree import ElementTree as Et
from halo import Halo


def extract_and_save(output: Path, total_points: int, filepaths: List[Path]):
    with h5py.File(output, "w") as f:
        first_array = extract_from_vtk(filepaths[0])
        f.create_dataset("data", 
            shape=(total_points, * first_array.shape[1::]),
            dtype=first_array.dtype,
            chunks=True) 
        f["data"][0] = first_array

        for i, vtk_file in enumerate(filepaths, start = 1):
            array = extract_from_vtk(vtk_file)
            f["data"][i] = array 

@Halo(text="processing raw dataset...")
def process_airfrans(input_dir: Path, output: Path):
    total_points = 0
    filepaths: List[Path] = []
    parser = Et()
    for subfolder in os.listdir(input_dir):
        filename = subfolder + "_internal.vtu"
        filepath = input_dir / subfolder / filename

        total_points += extract_num_points_from_xml(filepath, parser)
        filepaths.append(filepath)
    
    extract_and_save(output, total_points, filepaths)

    
