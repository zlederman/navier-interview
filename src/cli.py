from halo import Halo
from typing import List
from pathlib import Path


from src.io import download_zip, extract_zip
from src.constants import EXTRACTED_DATA_PATH, ZIP_PATH, UNZIP_PATH
from src.process.airfrans import process_airfrans


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
    setup([EXTRACTED_DATA_PATH, ZIP_PATH, UNZIP_PATH])
    spinner.text = f"downloading raw dataset to {ZIP_PATH}"
    spinner.start()
    # download_zip(ZIP_PATH, spinner)
    spinner.text = f"extracting zip files to {UNZIP_PATH}"
    extract_zip(ZIP_PATH, UNZIP_PATH, spinner, cleanup=False)
    process_airfrans(UNZIP_PATH, EXTRACTED_DATA_PATH)
    # spinner.stop()
    
