from pathlib import Path
import pyvista as pv
from xml.etree.ElementTree import ElementTree as ET
from numpy.typing import NDArray
import numpy as np

def extract_num_points_from_xml(filename: str, parser: ET) -> int:
    root = parser.parse(filename)
    piece = root.find("UnstructuredGrid/Piece")
    return int(piece.get("NumberOfPoints"))
            
def extract_from_vtk(filename: Path) -> NDArray:
    grid = pv.read(filename)
    dataset = np.empty((grid.n_points, 5), '<f8')

    # extract the relevant point data and add it to the array 
    dataset[:, 0:2] = grid.points[:, 0: 2]
    # extract the sdf 
    if "implicit_distance" in grid.point_data:
        sdf_data = grid.point_data["implicit_distance"]
        dataset[:, 2] = sdf_data
    
    # extract velocity data into the 4th and 5th columns
    if "U" in grid.point_data:
        velocity_data = grid.point_data["U"]
        dataset[:, 3: 5] = velocity_data[:, 0: 2]

        
    return dataset

