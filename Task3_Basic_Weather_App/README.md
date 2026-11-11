# Basic Weather App

A command-line app that looks up a place by name and shows its current temperature, apparent temperature, humidity, wind speed, and a short condition description.

## Run

From this folder, run:

    python weather_app.py

Enter a city or place name when prompted. Add a country or region to help distinguish locations with the same name, for example "Springfield, Illinois".

## Data source and privacy

The app uses Open-Meteo's public geocoding and forecast APIs. It sends the place name to the geocoding service, then requests current conditions for the returned coordinates. No API key or third-party Python package is needed. An internet connection is required. See the [Geocoding API documentation](https://open-meteo.com/en/docs/geocoding-api) and [Weather Forecast API documentation](https://open-meteo.com/en/docs).

The forecast API response can differ by location and model. If the service is unavailable, the app displays a short error instead of a traceback.

## Check

Run:

    python -m unittest -v

Automated tests use simulated API responses and do not make live requests.
