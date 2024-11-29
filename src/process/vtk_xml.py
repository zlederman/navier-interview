from pathlib import Path
import pyvista as pv
from xml.etree.ElementTree import ElementTree as ET
from numpy.typing import NDArray
import numpy as np
import re

def extract_num_points_from_file(filename: Path) -> int:
    with open(filename, 'r') as fp:
        raw = fp.read()
        match = re.search(r'Piece NumberOfPoints="(?P<num_points>\d+)"', raw)
        if match:
            return int(match.groupdict().get("num_points",0))
        return 0
            
    return int(piece.get("NumberOfPoints"))
            
def extract_from_vtk(filename: Path) -> NDArray:
    grid = pv.read(filename)
    dataset = np.empty((grid.n_points, 5), '<f8')

    # extract the relevant point data and add it to the array 
    dataset[:, 0:2] = grid.points[:, 0: 2].copy()
    # extract the sdf 
    if "implicit_distance" in grid.point_data:
        sdf_data = grid.point_data["implicit_distance"]
        dataset[:, 2] = sdf_data.copy()
    
    # extract velocity data into the 4th and 5th columns
    if "U" in grid.point_data:
        velocity_data = grid.point_data["U"]
        dataset[:, 3: 5] = velocity_data[:, 0: 2].copy()

    del grid
    return dataset

