import logging
import argparse
from datetime import date

import rasterio
import numpy as np
from shapely.geometry import Point

parser.add_argument('lon', type=float)
parser.add_argument('lat', type=float)
parser.add_argument('-b', '--buffer', type=float, default=0.01)
parser.add_argument('-d', '--date', type=date.fromisoformat)
parser.add_argument('-g', '--green', type=float, default=0.2)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.INFO)

# Creating circle from point
geometry = (args.lon, args.lat)
geometry = Point(geometry)
geometry = geometry.buffer(args.buffer)

# Searching
item = search(geometry, args.date)

red, nir = item.asset('B4'), item.asset('B5')
red, nir = red['href'], nir['href']

# Reading rasters
with rasterio.open(red) as src:
    redfile = mask(geometry, src)
with rasterio.open(nir) as src:
    nirfile = mask(geometry, src)

# Calculating NDVI
ndvifile = ndvi(redfile, nirfile)
with rasterio.open(ndvifile.name) as src:
    data = src.read()

total = np.size(data)
green = np.size()
