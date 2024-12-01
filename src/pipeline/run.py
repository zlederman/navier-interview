import asyncio
from functools import partial
import logging
from pathlib import Path
from typing import Dict
import zipfile
import requests
import os
from tqdm import tqdm
import concurrent.futures as cf

from src.models import ConfigModel, PipelineStates
from src.pipeline.process.airfrans import process_airfrans


def extract_zip(zip_path: Path, unzip_path: Path, cleanup: bool = False) -> Path:
    """
    zip_path: path to the zipped dataset
    unzip_path: path to directory in which to place unzipped files
    cleanup: bool = False to remove the zip file bc its huge
    returns:
        - the sub directory of the extracted data
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file in tqdm(zip_ref.filelist):
            zip_ref.extract(file, unzip_path)
    if cleanup:
        os.remove(zip_path)

    return unzip_path / "Dataset"


def download_zip(zip_path: Path):
    """
    zip_path: path to the zip file in which to download into
    spinner: for visualization

    downloads a zip file and tracks progress
    """
    res = requests.get(
        "https://data.isir.upmc.fr/extrality/NeurIPS_2022/Dataset.zip", stream=True
    )
    res.raise_for_status()

    unit = pow(2, 20)
    total_mib = int(res.headers.get("content-length", 0)) / unit
    pbar = tqdm(total=total_mib, unit="MiB", disable=True)

    with open(zip_path, "wb") as fp:
        for chunk in res.iter_content(chunk_size=8192):
            fp.write(chunk)
            pbar.update(len(chunk) / unit)


def run_pipeline_sync(config: ConfigModel, task_id: str, states: dict):
    states[task_id] = PipelineStates.STARTED_JOB
    # sets up working directories to place data
    logging.info("setting up your directories")
    states[task_id] = PipelineStates.SETTING_UP_DIR
    config.build_paths()
    # downloads zip file to target path
    logging.info(f"downloading raw dataset to {config.zip_path}")
    states[task_id] = PipelineStates.DOWNLOADING_ZIP
    download_zip(config.zip_path)
     # extracting zip into target folde
    logging.info(f"extracting zip files to {config.unzip_path}:")
    states[task_id] = PipelineStates.UNZIPPING_FILES
    extract_zip(config.zip_path, config.unzip_path, cleanup=False)
    # processing files
    logging.info(f"processing dataset and saving to {config.extracted_data_path}")
    states[task_id] = PipelineStates.PROCESSING_FILES
    stats = process_airfrans(config.unzip_path / "Dataset", config.extracted_data_path)
    
    states[task_id] = PipelineStates.JOB_COMPLETE


async def run_pipeline(
        config: ConfigModel, 
        task_id: str, 
        states: Dict[str, PipelineStates],
        active_tasks: Dict[str, asyncio.Task],
        thread_pool: cf.ThreadPoolExecutor
):
    '''async wrapper for running the pipeline in a thread pool'''
    try:
        # run the synchronous pipeline in a thread pool
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            thread_pool, 
            partial(run_pipeline_sync, config, task_id, states)
        )
    finally:
        if task_id in active_tasks:
            del active_tasks[task_id]