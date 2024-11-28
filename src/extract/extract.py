from pathlib import Path
import os
from src.extract.vtk_xml import extract_from_vtk, extract_num_points_from_xml
from typing import List
import h5py

def extract_to_h5(output_dir: Path, total_points: int, filepaths: List[Path]):

    with h5py.File(output_dir / "airfrans_data.h5", "w") as f:
        first_array = extract_from_vtk(filepaths[0])
        f.create_dataset("data", 
                        shape=(total_points, * first_array.shape[1::]),
                        dtype=first_array.dtype,
                        chunks=True) 
        f["data"][0] = first_array

        for i, vtk_file in enumerate(filepaths, start = 1):
            array = extract_from_vtk(vtk_file)
            f["data"][i+1] = array 

def extract_airfrans(input_dir: Path, output_dir: Path):
    total_points = 0
    filepaths: List[Path] = []
    for subfolder in os.listdir(input_dir):
        filename = subfolder + "_internal.vtu"
        filepath = input_dir / subfolder / filename

        total_points += extract_num_points_from_xml(filepath)
        filepaths.append(filepath)
    
    extract_to_h5(output_dir, total_points, filepaths)

    
