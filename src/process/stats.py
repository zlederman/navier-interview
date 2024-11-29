import math
import numpy as np


class DatasetStatistics:
    total_datasets: int
    total_points: int 

    x_max: float
    x_min: float
    y_max: float
    y_min: float

    sdf_min: float
    sdf_max: float
    sdf_mean: float
    sdf_std: float

    vmag_min: float
    vmag_max: float
    vmag_mean: float 
    vmag_std: float 

    def __init__(self, total_datasets: int):
        '''
        class representing the statistics of the NACA dataset
        '''
        MIN, MAX = float("inf"), float("-inf")
        self.total_datasets = total_datasets
        self.total_points = 0

        self.x_min, self.x_max = MIN, MAX
        self.y_min, self.y_max = MIN, MAX
        
        self.sdf_min, self.sdf_max = MIN, MAX
        self.sdf_mean = 0.0
        self.sdf_std = np.nan

        self.vmag_min, self.vmag_max = MIN, MAX
        self.vmag_mean = 0.0
        self.vmag_std = np.nan

    def update_min(self, value: float, field_name: str):
        attr = self.__getattribute__(field_name)
        if value < attr:
            self.__setattr__(field_name, value)

    def update_max(self, value: float, field_name: str):
        attr = self.__getattribute__(field_name)
        if value > attr:
            self.__setattr__(field_name, value)

    def update_average(self, sum: int, new_points: int, field_name: str):
        attr = self.__getattribute__(field_name)
        new_avg = attr * ((self.total_points  - new_points)/ self.total_points) + sum / self.total_points
        self.__setattr__(field_name, new_avg)

    def update_std(self):
        raise NotImplementedError
    

    def consume_dataset(self, dataset):
        length, _ = dataset.shape
        self.total_points += length
        array = np.apply_along_axis(
            func1d=lambda row: math.sqrt(row[0]**2 + row[1]**2) , axis=1, arr=dataset[:, 3:5])
        
        vmag_sum = np.sum(array)
        vmag_max, vmag_min = np.max(array), np.min(array)
        self.update_average(vmag_sum, length,"vmag_mean")
        self.update_max(vmag_max, "vmag_max")
        self.update_min(vmag_min, "vmag_min")

        xmin, xmax = np.min(dataset[:,0]), np.max(dataset[:,0])
        self.update_min(xmin, "x_min")
        self.update_max(xmax, "x_max")

        ymin, ymax = np.min(dataset[:,1]), np.max(dataset[:,1])
        self.update_min(ymin, "y_min")
        self.update_max(ymax, "y_max")

        sdf_sum = np.sum(dataset[:, 2])
        sdf_min, sdf_max = np.min(dataset[:,2]), np.max(dataset[:,2])
        self.update_average(sdf_sum, length, "sdf_mean")
        self.update_min(sdf_min, "sdf_min")
        self.update_max(sdf_max, "sdf_max")

    def __str__(self) -> str:
        return (
            f"Dataset Statistics:\n"
            f"  Datasets: {self.total_datasets:,d}\n"
            f"  Points: {self.total_points:,d}\n\n"
            f"  X Range: [{self.x_min:.3f}, {self.x_max:.3f}]\n"
            f"  Y Range: [{self.y_min:.3f}, {self.y_max:.3f}]\n\n"
            f"  SDF Stats:\n"
            f"    Range: [{self.sdf_min:.3f}, {self.sdf_max:.3f}]\n"
            f"    Mean:  {self.sdf_mean:.3f}\n"
            f"    Std:   {self.sdf_std:.3f}\n\n"
            f"  Velocity Magnitude Stats:\n"
            f"    Range: [{self.vmag_min:.3f}, {self.vmag_max:.3f}]\n"
            f"    Mean:  {self.vmag_mean:.3f}\n"
            f"    Std:   {self.vmag_std:.3f}"
        )
