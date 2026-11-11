"""A small command-line current weather app using Open-Meteo."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT_SECONDS = 10

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


class WeatherError(Exception):
    """Raised for a failed lookup or an unexpected weather response."""


@dataclass(frozen=True)
class WeatherReport:
    place: str
    country: str
    local_time: str
    temperature_c: float
    apparent_temperature_c: float | None
    relative_humidity_percent: int | None
    wind_speed_kmh: float | None
    condition: str


def _request_json(url: str, params: dict[str, str], opener=None) -> dict:
    """Fetch and decode one JSON API response."""
    request_url = f"{url}?{urlencode(params)}"
    request = Request(
        request_url,
        headers={"User-Agent": "OIBSIP-BasicWeatherApp/1.0 (educational project)"},
    )
    open_url = opener or urlopen
    try:
        with open_url(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read()
    except HTTPError as exc:
        raise WeatherError(f"The weather service returned HTTP {exc.code}.") from None
    except (URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "reason", None)
        detail = str(reason or exc)
        raise WeatherError(f"Could not reach the weather service: {detail}") from None

    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise WeatherError("The weather service returned invalid JSON.") from None
    if not isinstance(payload, dict):
        raise WeatherError("The weather service returned an unexpected response.")
    if payload.get("error"):
        reason = payload.get("reason", "The request was rejected.")
        raise WeatherError(f"The weather service could not complete the request: {reason}")
    return payload


def _as_float(value, label: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise WeatherError(f"The weather response did not include a valid {label}.") from None


def current_weather(place_name: str, opener=None) -> WeatherReport:
    """Find a place and retrieve its current weather conditions."""
    query = place_name.strip()
    if not query:
        raise ValueError("Please enter a place name.")

    location_data = _request_json(
        GEOCODING_URL,
        {"name": query, "count": "1", "language": "en", "format": "json"},
        opener,
    )
    results = location_data.get("results")
    if not isinstance(results, list) or not results:
        raise WeatherError(f"No matching place was found for {query!r}.")

    location = results[0]
    if not isinstance(location, dict):
        raise WeatherError("The geocoding service returned an unexpected place.")
    latitude = _as_float(location.get("latitude"), "latitude")
    longitude = _as_float(location.get("longitude"), "longitude")

    forecast_data = _request_json(
        FORECAST_URL,
        {
            "latitude": str(latitude),
            "longitude": str(longitude),
            "current": (
                "temperature_2m,relative_humidity_2m,apparent_temperature,"
                "weather_code,wind_speed_10m"
            ),
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "auto",
        },
        opener,
    )
    current = forecast_data.get("current")
    if not isinstance(current, dict):
        raise WeatherError("The forecast service did not return current conditions.")

    temperature = _as_float(current.get("temperature_2m"), "temperature")
    apparent = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")
    wind_speed = current.get("wind_speed_10m")
    code = current.get("weather_code")
    try:
        code_value = int(code)
    except (TypeError, ValueError):
        raise WeatherError("The forecast service did not return a valid weather code.") from None

    try:
        apparent_value = float(apparent) if apparent is not None else None
        humidity_value = int(humidity) if humidity is not None else None
        wind_value = float(wind_speed) if wind_speed is not None else None
    except (TypeError, ValueError):
        raise WeatherError("The forecast service returned invalid current conditions.") from None

    place = str(location.get("name") or query)
    country = str(location.get("country") or "")
    return WeatherReport(
        place=place,
        country=country,
        local_time=str(current.get("time") or "Not provided"),
        temperature_c=temperature,
        apparent_temperature_c=apparent_value,
        relative_humidity_percent=humidity_value,
        wind_speed_kmh=wind_value,
        condition=WEATHER_CODES.get(code_value, f"Unknown condition (code {code_value})"),
    )


def format_report(report: WeatherReport) -> str:
    title = ", ".join(part for part in (report.place, report.country) if part)
    lines = [
        f"Current weather for {title}",
        f"Local time: {report.local_time}",
        f"Condition: {report.condition}",
        f"Temperature: {report.temperature_c:.1f} °C",
    ]
    if report.apparent_temperature_c is not None:
        lines.append(f"Feels like: {report.apparent_temperature_c:.1f} °C")
    if report.relative_humidity_percent is not None:
        lines.append(f"Relative humidity: {report.relative_humidity_percent}%")
    if report.wind_speed_kmh is not None:
        lines.append(f"Wind speed: {report.wind_speed_kmh:.1f} km/h")
    return "\n".join(lines)


def main() -> int:
    try:
        place_name = input("Enter a city or place: ")
        report = current_weather(place_name)
    except (EOFError, KeyboardInterrupt):
        print("\nWeather lookup cancelled.")
        return 1
    except (ValueError, WeatherError) as exc:
        print(f"Error: {exc}")
        return 1

    print()
    print(format_report(report))
    print("\nWeather data: Open-Meteo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
