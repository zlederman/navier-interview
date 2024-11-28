
from src.extract.vtk_xml import extract_from_vtk, extract_num_points_from_xml
from xml.etree.ElementTree import ElementTree as Et

def test_xml_parser():
    filename = 'test/data/internal_sample.vtu'
    dataset = extract_from_vtk(filename, ["U", "implicit_distance"])
    assert dataset.shape == (180790, 5)


def test_xml_num_points():
    filename = 'test/data/internal_sample.vtu'

    num_points = extract_num_points_from_xml(filename, Et())
    assert num_points == 180790