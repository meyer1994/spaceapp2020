import logging
import tempfile
from typing import IO
from datetime import date

import rasterio

logger = logging.getLogger('datasets')
logger.setLevel(logging.INFO)


def lonlat(x: float, y: float, filename: str):
    logger.info('Reading file: %s', filename)
    with rasterio.open(filename, 'r') as src:
        coord = (x, y)
        sample = src.sample([coord])
        sample = next(sample)[0]
        return float(sample)


def carbon(x: float, y: float, day: date = None) -> float:
    filename = 'nasa/data/MOP_CO_M_2017-02-01_rgb_1440x720.FLOAT.TIFF'
    return lonlat(x, y, filename)


def aerosol(x: float, y: float, day: date = None):
    filename = 'nasa/data/MODAL2_M_AER_RA_2016-09-01_rgb_3600x1800.FLOAT.TIFF'
    return lonlat(x, y, filename)


def nitrogen(x: float, y: float, day: date = None):
    filename = 'nasa/data/AURA_NO2_M_2020-09-01_rgb_3600x1800.FLOAT.TIFF'
    return lonlat(x, y, filename)
