import os
import time

import requests

from src.api import fetch_weather
from src.database import init_database, store_api_data


def run_pipeline(cycle_number):
    print(f"\n--- Starting cycle {cycle_number} ---")

    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError(
            "WEBHOOK_URL is not set. Add it as an environment variable."
        )

    data = fetch_weather()
    print("API data fetched successfully")

    store_api_data(data)
    print("API data stored successfully")

    response = requests.post(webhook_url, json=data, timeout=10)
    response.raise_for_status()

    print("Data sent to webhook successfully")
    print(f"Cycle {cycle_number} completed successfully")
    return True


def run_automation(cycles=3, interval_seconds=30):
    if cycles < 1:
        raise ValueError("cycles must be at least 1")
    if interval_seconds < 0:
        raise ValueError("interval_seconds cannot be negative")

    init_database()

    for cycle_number in range(1, cycles + 1):
        run_pipeline(cycle_number)

        if cycle_number < cycles:
            print(
                f"Waiting {interval_seconds} seconds before the next cycle..."
            )
            time.sleep(interval_seconds)
