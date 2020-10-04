from datetime import date, timedelta

import rasterio
from fastapi import FastAPI
from pydantic import BaseModel

from nasa.services import climate
from nasa.services import landsat
from nasa.services import datasets

app = FastAPI()


@app.get('/green')
async def get_green(x: float, y: float, day: date):
    return landsat.green(x, y, day)


@app.get('/datasets')
async def get_datasets(x: float, y: float, day: date = None):
    return {
        'carbon_monoxide': datasets.carbon(x, y),
        'aerosol_particles': datasets.aerosol(x, y),
        'nitrogen_dioxide': datasets.nitrogen(x, y),
        'uvindex': datasets.uvindex(x, y),
    }


@app.get('/temperature')
async def get_temperature(x: float, y: float, day: date):
    return climate.temperature(x, y, day)
