from datetime import date, timedelta

import rasterio
from fastapi import FastAPI
from pydantic import BaseModel

from nasa.services import landsat

app = FastAPI()


@app.get('/green')
async def green(x: float, y: float, day: date):
    return {'vegetation': landsat.green(x, y, day)}
