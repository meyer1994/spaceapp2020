import os
import contextlib
from datetime import date

import httpx

KEY = os.environ['OPENWEATHER_KEY']
URL = 'http://history.openweathermap.org/data/2.5/history/city'


def temperature(x: float, y: float, day: date) -> dict:
    params = {
        'lat': y,
        'lon': x,
        'type': 'hour',
        'start': str(day),
        'cnt': 1,
        'appid': KEY,
    }
    response = httpx.get(URL, params=params)
    return response.json()

