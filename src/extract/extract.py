from pathlib import Path
import os
from src.extract.filename import parse_filename
from src.extract.internal_vtu import extract_internal_vtu_file

def extract_airfrans(input_dir: Path, output_dir: Path):
    for subfolder in os.listdir(input_dir):
        metadata = parse_filename(subfolder)
        
        # open up the internal vtu file 
        filename = metadata.filename + "_internal.vtu"
        with open(input_dir / subfolder / filename, 'r') as fp:
            df = extract_internal_vtu_file()
            