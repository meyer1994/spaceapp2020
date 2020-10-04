import shutil
import logging
import argparse
from datetime import date

import rasterio

from nasa.services import landsat

parser = argparse.ArgumentParser()
parser.add_argument('x', type=float)
parser.add_argument('y', type=float)
parser.add_argument('date', type=date.fromisoformat)
parser.add_argument('-b', '--buffer', type=float, default=0.01)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

geometry = landsat.circle(args.x, args.y, args.buffer)
item = landsat.search(geometry, args.date)
red, nir, grn = item.asset('B4'), item.asset('B5'), item.asset('B3'),
red, nir, grn = red['href'], nir['href'], grn['href']
with rasterio.open(red) as src:
    red = landsat.mask(geometry, src)
with rasterio.open(nir) as src:
    nir = landsat.mask(geometry, src)
with rasterio.open(grn) as src:
    grn = landsat.mask(geometry, src)
ndvi = landsat.ndvi(red, nir)

shutil.copy(ndvi.name, 'ndvi.tif')
shutil.copy(red.name, 'red.tif')
shutil.copy(nir.name, 'nir.tif')
shutil.copy(grn.name, 'grn.tif')
