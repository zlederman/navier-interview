
from pathlib import Path
import zipfile
import requests
from halo import Halo
import os

def extract_zip(zip_path: Path, unzip_path: Path, spinner: Halo, cleanup: bool = False) -> Path: 
    '''
    zip_path: path to the zipped dataset
    unzip_path: path to directory in which to place unzipped files
    cleanup: bool = False to remove the zip file bc its huge
    returns:
        - the sub directory of the extracted data
    '''
    files_extracted = 0
    percent = 0.0
    base_str = spinner.text

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_files = len(zip_ref.filelist)
        for file in zip_ref.filelist:
            
            location = zip_ref.extract(file, unzip_path)
            # fs operations to ensure zip gets extracted to correct directory
            files_extracted += 1
            percent = (files_extracted / total_files) * 100
            spinner.text = base_str + f" {percent:.1f}" + "%"

    if cleanup:
        os.remove(zip_path)

    return unzip_path / "Dataset"   
       
def download_zip(zip_path: Path, spinner: Halo):
    '''
        zip_path: path to the zip file in which to download into
        spinner: for visualization

        downloads a zip file and tracks progress
    '''
    res = requests.get("https://data.isir.upmc.fr/extrality/NeurIPS_2022/Dataset.zip", stream=True)

    unit = pow(2, 20)
    total_mib = int(res.headers.get("content-length", 0)) / unit
    chunk_size = 8192
    downloaded_mib = 0

    base_str = spinner.text
    with open(zip_path, 'wb') as fp:
        for chunk in res.iter_content(chunk_size=8192):
            
            fp.write(chunk) 
            downloaded_mib += chunk_size / unit
            percentage = (downloaded_mib / total_mib) * 100
            spinner.text = base_str + f" {percentage:.1f}" + "%"
            

    