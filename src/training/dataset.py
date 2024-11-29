import torch
from pathlib import Path
import h5py


class NACAPositionVelocityDataset(torch.utils.data.Dataset):

    def __init__(self, data_path: Path, dataset_name: str):
        self.data_path = data_path
        self.h5_file = h5py.File(data_path, mode="r")
        self.data = self.h5_file[dataset_name]
        self.length, self.width = self.data.shape

    def __len__(self):
        return self.length

    def __del__(self):
        self.h5_file.close()

    def __getitem__(self, index):
        features = torch.tensor(self.data[index, 0 : self.width - 2])
        targets = torch.tensor(self.data[index, self.width - 2 : :])
        return features, targets
