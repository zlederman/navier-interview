from src.extract.filename import parse_filename

def test_parse_filenames_basic():
    filename = "airFoil2D_SST_31_13_3_3_6"
    metadata = parse_filename(filename)
    assert metadata.inlet_velocity == 31.0
    assert metadata.attack_angle == 13.0
    assert metadata.naca_series == 4.0
    assert metadata.naca_code == (3.0,3.0,6.0)

def test_parse_filenames_floats():
    filename = "airFoil2D_SST_43.597_5.932_3.551_3.1_1.0_18.252"
    metadata = parse_filename(filename)
    assert metadata.inlet_velocity == 43.597
    assert metadata.attack_angle == 5.932
    assert metadata.naca_series == 5
    assert metadata.naca_code == (3.551, 3.1, 1.0, 18.252)

def test_parse_filenames_neg():
    filename = "airFoil2D_SST_91.707_-1.557_3.933_4.731_0.0_12.944"
    metadata = parse_filename(filename)
    assert metadata.inlet_velocity == 91.707
    assert metadata.attack_angle == -1.557
    assert metadata.naca_series == 5
    assert metadata.naca_code == (3.933, 4.731, 0.0, 12.944)
