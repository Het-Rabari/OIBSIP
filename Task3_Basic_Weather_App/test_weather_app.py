import json
import unittest
from urllib.parse import parse_qs, urlparse
from urllib.error import URLError

try:
    from .weather_app import (
        FORECAST_URL,
        GEOCODING_URL,
        WeatherError,
        current_weather,
        format_report,
    )
except ImportError:
    from weather_app import (
        FORECAST_URL,
        GEOCODING_URL,
        WeatherError,
        current_weather,
        format_report,
    )


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class WeatherAppTests(unittest.TestCase):
    def test_fetches_place_and_formats_current_conditions(self):
        requests = []
        responses = [
            {
                "results": [
                    {
                        "name": "Pune",
                        "country": "India",
                        "latitude": 18.5204,
                        "longitude": 73.8567,
                    }
                ]
            },
            {
                "current": {
                    "time": "2026-11-11T18:00",
                    "temperature_2m": 24.5,
                    "apparent_temperature": 25.1,
                    "relative_humidity_2m": 62,
                    "weather_code": 2,
                    "wind_speed_10m": 8.4,
                }
            },
        ]

        def fake_opener(request, timeout):
            requests.append((request, timeout))
            return FakeResponse(responses.pop(0))

        report = current_weather("Pune", opener=fake_opener)

        self.assertEqual(report.place, "Pune")
        self.assertEqual(report.country, "India")
        self.assertEqual(report.condition, "Partly cloudy")
        self.assertEqual(report.temperature_c, 24.5)
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0][1], 10)
        self.assertEqual(urlparse(requests[0][0].full_url).scheme, "https")
        self.assertTrue(requests[0][0].full_url.startswith(GEOCODING_URL))
        self.assertTrue(requests[1][0].full_url.startswith(FORECAST_URL))
        forecast_query = parse_qs(urlparse(requests[1][0].full_url).query)
        self.assertEqual(forecast_query["temperature_unit"], ["celsius"])
        self.assertEqual(forecast_query["timezone"], ["auto"])
        self.assertIn("Feels like: 25.1 °C", format_report(report))
        self.assertIn("Relative humidity: 62%", format_report(report))

    def test_rejects_empty_place_without_a_request(self):
        with self.assertRaises(ValueError):
            current_weather("   ", opener=lambda *_args, **_kwargs: self.fail("network call"))

    def test_reports_no_matching_place(self):
        with self.assertRaisesRegex(WeatherError, "No matching place"):
            current_weather("No Such Place", opener=lambda *_args, **_kwargs: FakeResponse({}))

    def test_reports_network_failure(self):
        def failed_opener(_request, timeout):
            raise URLError("offline")

        with self.assertRaisesRegex(WeatherError, "Could not reach"):
            current_weather("Pune", opener=failed_opener)

    def test_reports_invalid_json(self):
        class InvalidJsonResponse(FakeResponse):
            def __init__(self):
                self.body = b"not-json"

        with self.assertRaisesRegex(WeatherError, "invalid JSON"):
            current_weather(
                "Pune",
                opener=lambda _request, timeout: InvalidJsonResponse(),
            )


if __name__ == "__main__":
    unittest.main()
