import copy
import logging
import tempfile
from typing import IO
from datetime import date

import rasterio
import rasterio.crs
import rasterio.mask
import rasterio.warp
import rasterio.features
import numpy as np
from satsearch import Search
from shapely.geometry import Point

URL = 'https://earth-search.aws.element84.com/v0'
LANDSAT = 'landsat-8-l1-c1'
WGS84 = rasterio.crs.CRS.from_epsg(4326)

logger = logging.getLogger('landsat')


def circle(x: float, y: float, buff: float) -> dict:
    geometry = (x, y)
    geometry = Point(geometry)
    geometry = geometry.buffer(buff)
    return geometry.__geo_interface__


def search(geometry: dict, datetime: date) -> object:
    logger.info('Searching images')
    kwargs = {
        'intersects': geometry,
        'datetime': datetime.isoformat(),
        'collections': [LANDSAT]
    }
    search = Search(url=URL, **kwargs)
    items = search.items()
    logger.debug('Found: %d', len(items))
    return next(iter(items))


def mask(geometry: dict, src: object) -> IO:
    meta = copy.deepcopy(src.profile)

    logger.info('Reprojecting geometry')
    geometry = rasterio.warp.transform_geom(WGS84, src.crs, geometry)
    bounds = rasterio.features.bounds(geometry)

    logger.info('Masking raster')
    mask, transform = rasterio.mask\
        .mask(src, [geometry], crop=True, all_touched=True)
    bands, *shape = mask.shape

    logger.info('Reprojecting raster')
    transform_c, *shape_c = rasterio.warp\
        .calculate_default_transform(src.crs, WGS84, *shape, *bounds)
    shape_c = shape_c[::-1]  # I have no idea why

    dtype = meta.get('dtype')
    dest_shape = (bands, *shape_c)
    dest = np.zeros(dest_shape, dtype)
    image, transform = rasterio.warp\
        .reproject(mask, dest, src_transform=transform, src_crs=src.crs,
                   dst_transform=transform_c, dst_crs=WGS84)

    meta.update({
        'crs': WGS84,
        'driver': 'GTiff',
        'width': shape_c[1],
        'height': shape_c[0],
        'transform': transform_c,
        'nodata': 0.0,
    })

    logger.info('Writing raster')
    temp = tempfile.NamedTemporaryFile(suffix='.tif')
    with rasterio.open(temp.name, 'w', **meta) as dst:
        dst.write(image)

    return temp


def ndvi(redfile: object, nirfile: object) -> IO:
    logger.info('Reading data')
    with rasterio.open(redfile.name) as src:
        red = src.read()
    with rasterio.open(nirfile.name) as src:
        nir = src.read()

    logger.info('Calculating NDVI')
    top = (nir - red).astype('float32')
    bot = (nir + red).astype('float32')
    with np.errstate(invalid='ignore'):
        ndvi = np.where(bot == 0.0, 0.0, top / bot).astype('float32')

    logger.info('Writing NDVI')
    with rasterio.open(redfile.name) as red:
        meta = copy.deepcopy(red.profile)
        meta.update(dtype='float32')

    temp = tempfile.NamedTemporaryFile(suffix='.tif')
    with rasterio.open(temp.name, 'w', **meta) as dst:
        dst.write(ndvi)

    return temp


def green(x: float, y: float, day: date) -> float:
    geometry = circle(x, y, 0.01)

    item = search(geometry, day)
    red, nir = item.asset('B4'), item.asset('B5')
    red, nir = red['href'], nir['href']

    with rasterio.open(red) as src:
        red_file = mask(geometry, src)
    with rasterio.open(nir) as src:
        nir_file = mask(geometry, src)

    ndvi_file = ndvi(red_file, nir_file)
    with rasterio.open(ndvi_file.name) as src:
        data = src.read()

    size = np.size(data)
    vegetation = (data > 0.2).sum()

    return vegetation / size
