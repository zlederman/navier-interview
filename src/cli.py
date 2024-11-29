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
    spinner = Halo(text='setting up...', spinner='dots')
    # sets up working directories to place data
    setup([EXTRACTED_DATA_PATH, ZIP_PATH, UNZIP_PATH])
    spinner.text = f"downloading raw dataset to {ZIP_PATH}"
    spinner.start()
    #downloads zip file to target path, includes spinner for progress
    download_zip(ZIP_PATH, spinner)
    spinner.text = f"extracting zip files to {UNZIP_PATH}"
    # extracting zip into target folder
    extract_zip(ZIP_PATH, UNZIP_PATH, spinner, cleanup=False)
    spinner.text = f"processing dataset and saving to {EXTRACTED_DATA_PATH}"
    stats = process_airfrans(UNZIP_PATH / "Dataset", EXTRACTED_DATA_PATH)
    spinner.stop()
    print(stats)
    
