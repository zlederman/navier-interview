from halo import Halo
from typing import List
from pathlib import Path


from src.io import download_zip, extract_zip
from src.process.airfrans import process_airfrans

BASE_PATH = Path("data")
ZIP_PATH = BASE_PATH / "zip" / "naca_raw.zip"
UNZIP_PATH = BASE_PATH / "naca_raw"
EXTRACTED_DATA_PATH = BASE_PATH / "extracted" / "naca_position_sdf_velocity.h5"


def setup(paths: List[Path]):
    '''
        sets up working directories
    '''
    for path in paths:
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # sets up working directories to place data
    print("* setting up your directories")
    setup([EXTRACTED_DATA_PATH, ZIP_PATH, UNZIP_PATH])
    print(f"* downloading raw dataset to {ZIP_PATH}")
    #downloads zip file to target path
    download_zip(ZIP_PATH)
    print(f"* extracting zip files to {UNZIP_PATH}:")
    #extracting zip into target folder
    extract_zip(ZIP_PATH, UNZIP_PATH, cleanup=False)
    print(f"* processing dataset and saving to {EXTRACTED_DATA_PATH}")
    stats = process_airfrans(UNZIP_PATH / "Dataset", EXTRACTED_DATA_PATH)
    print(stats)
    
