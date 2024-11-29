from src.process.vtk_xml import extract_num_points_from_file
from src.process.vtk_xml import extract_from_vtk
from src.process.stats import DatasetStatistics
from xml.etree.ElementTree import ElementTree as Et
from pathlib import Path
import numpy as np
import math


def test_xml_num_points():
    filename = "test/data/sample/sample_internal.vtu"
    num_points = extract_num_points_from_file(filename)
    assert num_points == 180790


def test_stats_single_file():
    stats = DatasetStatistics(1)
    dataset = extract_from_vtk("test/data/sample/sample_internal.vtu")
    length, width = dataset.shape
    stats.consume_dataset(dataset)
    array = np.apply_along_axis(
        func1d=lambda row: math.sqrt(row[0] ** 2 + row[1] ** 2),
        axis=1,
        arr=dataset[:, 3:5],
    )
    vmag_max, vmag_min = np.max(array), np.min(array)
    xmin, xmax = np.min(dataset[:, 0]), np.max(dataset[:, 0])
    ymin, ymax = np.min(dataset[:, 1]), np.max(dataset[:, 1])
    sdf_min, sdf_max = np.min(dataset[:, 2]), np.max(dataset[:, 2])
    sdf_sum = np.mean(dataset[:, 2]) * length
    assert sdf_sum / length - stats.sdf_mean <= 1e-4
    assert stats.sdf_max == sdf_max and stats.sdf_min == sdf_min
    assert stats.x_max == xmax and stats.x_min == xmin
    assert stats.y_max == ymax and stats.y_min == ymin
    assert stats.vmag_max == vmag_max and stats.vmag_min == vmag_min


def test_stats_two_files():
    stats = DatasetStatistics(2)
    dataset = extract_from_vtk("test/data/sample/sample_internal.vtu")
    dataset_2 = extract_from_vtk("test/data/sample/sample2_internal.vtu")

    # tell stats obj to consume dataset
    stats.consume_dataset(dataset)
    stats.consume_dataset(dataset_2)
    # make large dataset
    dataset = np.concat([dataset, dataset])

    array = np.apply_along_axis(
        func1d=lambda row: math.sqrt(row[0] ** 2 + row[1] ** 2),
        axis=1,
        arr=dataset[:, 3:5],
    )
    vmag_max, vmag_min = np.max(array), np.min(array)

    xmin, xmax = np.min(dataset[:, 0]), np.max(dataset[:, 0])
    ymin, ymax = np.min(dataset[:, 1]), np.max(dataset[:, 1])

    sdf_min, sdf_max = np.min(dataset[:, 2]), np.max(dataset[:, 2])
    sdf_mean = np.mean(dataset[:, 2])
    sdf_std = np.std(dataset[:, 2])

    assert sdf_mean - stats.sdf_mean <= 1e-4
    assert stats.sdf_max == sdf_max and stats.sdf_min == sdf_min
    assert stats.x_max == xmax and stats.x_min == xmin
    assert stats.y_max == ymax and stats.y_min == ymin
    assert stats.vmag_max == vmag_max and stats.vmag_min == vmag_min
    assert stats.sdf_std - sdf_std <= 1e-4
