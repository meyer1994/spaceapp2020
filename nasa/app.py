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
    carbon = datasets.carbon(x, y)
    aerosol = datasets.aerosol(x, y)
    nitrogen = datasets.nitrogen(x, y)
    green = landsat.green(x, y, day)
    return {
        'green': green,
        'carbon_monoxide': carbon,
        'aerosol_particles': aerosol,
        'nitrogen_dioxide': nitrogen,
    }


@app.get('/temperature')
async def get_temperature(x: float, y: float, day: date):
    return climate.temperature(x, y, day)
