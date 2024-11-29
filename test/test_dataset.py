from src.process.airfrans import process_airfrans
from src.training.dataset import NACAPositionVelocityDataset
from pathlib import Path
import os
def test_pytorch_dataset():
    path = Path("test/data/")
    h5_loc = Path("test/data/data.h5")
    process_airfrans(path, h5_loc)
    dataset = NACAPositionVelocityDataset(h5_loc, "data")
    train, test = dataset[0]
    assert train != test
    
    
