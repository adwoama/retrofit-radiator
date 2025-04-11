import json
import csv
import requests
from datetime import datetime, timedelta

# Insert your OpenWeatherMap API key here
API_KEY = "2c8400a2c235b7e5f3df60e6ba05bb98"
# Coordinates for CMU, e.g. (Pittsburgh)
LAT = 40.4443533
LON = -79.9435786
url = (
        "https://api.openweathermap.org/data/3.0/onecall/timemachine"
        f"?lat={LAT}&lon={LON}&dt={int(1744013391)}&appid={API_KEY}&units=metric"
    )
try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    print(data["current"]["temp"])  # Celsius
except Exception as e:
    print(f"Failed to fetch temperature for {1744013391} (timestamp={1744013391}): {e}")
        