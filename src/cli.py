from src.pipeline.config import ConfigModel
from src.pipeline.run import run_pipeline

def run_cli(args):
    # sets up working directories to place data
    config = ConfigModel(
        extractedDataPath=args.extracted_data_path,
        unzipPath=args.unzip_path,
        zipPath=args.zip_path
    )
    run_pipeline(config)
