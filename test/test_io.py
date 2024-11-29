from src.io import extract_zip
from pathlib import Path
from halo import Halo

def test_unzip_into_target_path():
    zip_path = Path('/Users/zach-mac/Documents/dev/navier-interview/data/zip/naca_raw.zip')
    unzip_path = Path('/Users/zach-mac/Documents/dev/navier-interview/data/unzip')
    halo = Halo()
    extract_zip(zip_path, unzip_path, halo)


