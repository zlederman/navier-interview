from typing import Tuple, Type
import xml
import numpy as np
from dataclasses import dataclass

NACA_4 = Tuple[float, float, float]
NACA_5 = Tuple[float, float, float, float]


@dataclass
class Metadata:
    inlet_velocity: float
    attack_angle: float
    naca_series: 4 | 5
    naca_code: NACA_4 | NACA_5
    filename: str


def parse_filename(filename: str):
    splits = filename.split("_")

    inlet_velocity = float(splits[2])
    attack_angle = float(splits[3])
    # handle naca
    NACA_IDX, naca_temp = 4, []
    naca_series = 5 if len(splits[NACA_IDX::]) == 4 else 4
    for i in range(naca_series - 1):
        naca_temp.append(float(splits[NACA_IDX + i]))
    naca_code = tuple(naca_temp)

    return Metadata(inlet_velocity, attack_angle, naca_series, naca_code, filename)
