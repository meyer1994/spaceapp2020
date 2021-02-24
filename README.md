# 2020 Challenge

[![build](https://github.com/meyer1994/spaceapp2020/actions/workflows/build.yml/badge.svg)](https://github.com/meyer1994/spaceapp2020/actions/workflows/build.yml)

Code used in SpaceApps 2020 NASA Hackaton

## Install

This program uses [gdal][1] to run. Be sure to have it installed. After that,
just install the python dependencies and you are good to go.

```bash
pip install -r requirements.txt
```

Or, if you prefer, you can simply build our docker image that is provided.

```bash
docker build . -t spaceapp2020
docker run --rm -it -e OPENWEATHER_KEY=<your-key> spaceapp2020
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

Of course, instead of using an commercial API as this one we could have used
NASA's datasets on earth temperature. But we choose to do so to save on time
for the hackathon.

#### `GET /datasets?x={lon}&y={lat}`

Returns available information from NASA datasets. This endpoint was created as
a way to show that it is entirely possible to create an easy way to interact
with data that is already available on the internet. It gets data from some
NASA datasets and return them in an easi way to understand and use in any
computer program.

```bash
http GET https://spaceapp2020.herokuapp.com/datasets x==-48.422 y==-27.573
{
    "aerosol_particles": 99999.0,
    "carbon_monoxide": 61.400001525878906,
    "nitrogen_dioxide": 106.0,
    "uvindex": 14.430000305175781
}
```

## Deployment

We have used [Heroku][3] as our hosting service. Mainly because of how easy is
to use it. To deploy, you will need to install [Heroku's CLI][4]. You will also
need an World Weather Online api key, if you want to use the temperature
endpoint. If not, the other endpoints will work fine. However, you can just use
the currently deployed version. Its url is:

```
https://spaceapp2020.herokuapp.com
```

To set the World Weather Online API key, just use:

```bash
heroku config:set OPENWEATHER_KEY="<YOUR_KEY>"
```

We use [Docker][5] container deployment. Not because it is easier, but because
we must. Heroku's Dynos do not come with GDAL installed. But they allow you to
send dockerfiles that are built and used to run your application. So we use a
dockerfile that has python and gdal already included.


[1]: https://gdal.org/
[2]: https://worldweatheronline.com/
[3]: https://heroku.com/
[4]: https://devcenter.heroku.com/articles/heroku-cli
[5]: https://docker.com/
