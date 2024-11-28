import os
from pathlib import Path
from dotenv import load_dotenv
from src.download.airfrans import download_airfrans_data
from src.extract.extract import extract_airfrans


def load_env():
    env_file = Path(".env")
    if os.path.exists(env_file):
        load_dotenv()
    else:
        print("please fill out .env file")
        with open(env_file, "w") as fp:
            fp.write("AIRFRANS_TASK=")
            fp.write("AIRFRANS_DATASET=")
            fp.write("AIRFRANS_DATASET_DIR=")
            fp.write("AIRFRANS_ZIP_FILENAME=")
        
def download():
    dataset_path = Path(os.environ["AIRFRANS_DATASET_DIR"])
    zip_file = os.environ["AIRFRANS_ZIP_FILENAME"]
    download_airfrans_data(
            dataset_path,
            zip_file,
            os.environ["AIRFRANS_TASK"],
            os.environ["AIRFRANS_DATASET"]
    )
    os.remove(dataset_path / zip_file) 

    
if __name__ == "__main__":
    load_env()
    download()
    extract_airfrans()
    
