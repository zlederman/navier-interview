from src.pipeline.config import ConfigModel
from src.pipeline.run import run_pipeline


# BASE_PATH = Path("data")
# ZIP_PATH = BASE_PATH / "zip" / "naca_raw.zip"
# UNZIP_PATH = BASE_PATH / "naca_raw"
# EXTRACTED_DATA_PATH = BASE_PATH / "extracted" / "naca_position_sdf_velocity.h5"






def run_cli(args):
    # sets up working directories to place data
    config = ConfigModel(
        extractedDataPath=args.extracted_data_path,
        unzipPath=args.unzip_path,
        zipPath=args.zip_path
    )
    run_pipeline(config)
