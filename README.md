# 2020 Challenge

Code used in a 2020 Nasa Challenge Hackaton

## Install
This program uses [gdal][1] to run. Be sure to have it installed. After that,
just install the python dependencies and you are good to go.

```bash
pip install -r requirements.txt
```

Or, if you prefer, you can simply build our docker image that is provided.

```bash
docker build .
```

## Usage
This prototype is a very simple HTTP server that has some useful endpoints that
can be used to fecth different carbon footprint related data for an specified
place and on some specified time. We will list the available endpoints below:

#### `GET /green?x={lon}&y={lat}&day={date}`
Returns percentage of vegetation and water near the specified point. If there
is no Landsat image for the passed day, it will return a 404. Note that this
endpoint performs the downloads of some raster data for calculations. So it can
take up to 20 seconds to complete.

The following example fetches some data from a point in Florianópolis, Brazil.

```bash
http GET https://spaceapp2020.herokuapp.com/green x==-48.422 y==-27.573 day==2020-09-11
{
    "vegetation": 0.29378858024691357,
    "water": 0.3333333333333333
}
```

If you try a day that is not available, it should return a 404:

```bash
http GET https://spaceapp2020.herokuapp.com/green x==-48.422 y==-27.573 day==2020-09-12
{
    "detail": "Image not found for date"
}
```

#### `GET /temperature?x={lon}&y={lat}&day={date}`
Returns historical temperature information from [World Weather Online][2].

```bash
http GET https://spaceapp2020.herokuapp.com/temperature x==-48.422 y==-27.573 day==2020-09-11
{
    "avgtempC": "22",
    "avgtempF": "72",
    "date": "2020-09-12",
    "maxtempC": "24",
    "maxtempF": "76",
    "mintempC": "18",
    "mintempF": "65",
    "sunHour": "11.6",
    "totalSnow_cm": "0.0",
    "uvIndex": "6"
}
```

[1]: https://www.gdal.org/
[2]: https://www.worldweatheronline.com/
