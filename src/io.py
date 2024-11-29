
from pathlib import Path
import zipfile
import requests
from halo import Halo
import os
from tqdm import tqdm

def extract_zip(zip_path: Path, unzip_path: Path, cleanup: bool = False) -> Path: 
    '''
    zip_path: path to the zipped dataset
    unzip_path: path to directory in which to place unzipped files
    cleanup: bool = False to remove the zip file bc its huge
    returns:
        - the sub directory of the extracted data
    '''
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in tqdm(zip_ref.filelist):
            zip_ref.extract(file, unzip_path)
    if cleanup:
        os.remove(zip_path)

    return unzip_path / "Dataset"   
       
def download_zip(zip_path: Path):
    '''
        zip_path: path to the zip file in which to download into
        spinner: for visualization

        downloads a zip file and tracks progress
    '''
    res = requests.get("https://data.isir.upmc.fr/extrality/NeurIPS_2022/Dataset.zip", stream=True)

    unit = pow(2, 20)
    total_mib = int(res.headers.get("content-length", 0)) / unit
    pbar = tqdm(total=total_mib, unit='MiB')
    chunk_size = 8192

    with open(zip_path, 'wb') as fp:
        for chunk in res.iter_content(chunk_size=8192):
            fp.write(chunk) 
            pbar.update(chunk_size / unit)
            

    