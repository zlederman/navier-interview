from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel
from pathlib import Path


class ConfigModel(BaseModel):
    extracted_data_path: Path = Field(alias="extractedDataPath")
    unzip_path: Path = Field(alias="unzipPath")
    zip_path: Path = Field(alias="zipPath")

    class Config:
        alias_generator = to_camel
        populate_by_alias = True


    def build_paths(self):
        kwargs = {"parents": True, "exist_ok": True}
        # sets up the parent directory for the zip file to save into
        self.zip_path.parent.mkdir(**kwargs)
        # sets up the directory to load all unzipped files
        self.unzip_path.mkdir(**kwargs)
        # sets up the parent to save the h5 file
        self.extracted_data_path.parent.mkdir(**kwargs)