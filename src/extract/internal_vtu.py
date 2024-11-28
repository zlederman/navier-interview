from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

def extract_internal_vtu_file(raw_xml: str) -> pd.DataFrame:
    root = ET.fromstring(raw_xml)
    compressor = root.find()
    return pd.DataFrame()


