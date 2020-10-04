import os
import contextlib
from datetime import date

import httpx

KEY = os.getenv('OPENWEATHER_KEY')
URL = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx'


def temperature(x: float, y: float, day: date) -> dict:
    params = {'q': f'{y},{x}', 'date': str(day), 'format': 'json', 'key': KEY}
    response = httpx.get(URL, params=params)
    return response.json()

