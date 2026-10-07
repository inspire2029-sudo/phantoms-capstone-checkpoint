import os

import requests


API_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather():
    """Fetch Alexandria weather using a key loaded from the environment."""
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not set. "
            "Add it as an environment variable."
        )

    params = {
        "q": "Alexandria,EG",
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=10,
    )
    response.raise_for_status()

    return response.json()
