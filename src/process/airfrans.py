from pathlib import Path
import os
from src.process.stats import DatasetStatistics
from src.process.vtk_xml import extract_from_vtk, extract_num_points_from_file
from typing import List
import h5py
from tqdm import tqdm


def extract_and_save(output: Path, total_points: int, filepaths: List[Path], stats: DatasetStatistics):
    '''        
    creates an h5 py file, but loads files one at a time as to avoid consuming too memory
        also tracks running statistics
    '''
    print("* extracting to h5d file")
    with h5py.File(output, "w") as f:
        dataset = extract_from_vtk(filepaths[0])
        stats.consume_dataset(dataset)
        length, width = dataset.shape
        f.create_dataset("data", 
                shape=(total_points, width),
                dtype=dataset.dtype,
                chunks=True) 
        
        f["data"][: length] = dataset
        cnt = length
        for i in tqdm(range(1, len(filepaths))):
            try:
                dataset = extract_from_vtk(filepaths[i])
                stats.consume_dataset(dataset)

                length, _ = dataset.shape
                f["data"][cnt: length + cnt] = dataset
                cnt += length 
            except:
                print(f"unable to extract vtk data from: {filepaths[i]}")



def process_airfrans(input_dir: Path, output: Path) -> DatasetStatistics:
    
    total_points = 0
    filepaths: List[Path] = []

    for subfolder in os.listdir(input_dir):
        filename = subfolder + "_internal.vtu"
        filepath = input_dir / subfolder / filename
        if filepath.exists():
            points = extract_num_points_from_file(filepath)
            if points == 0:
                # skip files where we cant find the correct number of points
                continue
            total_points += points
    
            filepaths.append(filepath)
            
    stats = DatasetStatistics(len(filepaths))
    extract_and_save(output, total_points, filepaths, stats)

    return stats

    
