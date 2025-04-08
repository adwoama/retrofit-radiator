import json
import csv
import requests
from datetime import datetime, timedelta
from api_key import API_KEY  # Assuming you have a separate file for your API key

# Insert your OpenWeatherMap API key here
API_KEY = API_KEY
# Coordinates for CMU, e.g. (Pittsburgh)
LAT = 40.4443533
LON = -79.9435786

def get_outdoor_temp_utc(timestamp):
    """
    Fetches the outdoor temperature (°C) from OpenWeatherMap at the given UTC timestamp.
    Returns "N/A" if the timestamp is older than 5 days or in the future.
    """
    dt = datetime.utcfromtimestamp(timestamp)
    now = datetime.utcnow()
    diff = now - dt

    # If dt is more than 5 days in the past or in the future, return "N/A"
    if diff > timedelta(days=5) or diff.days < 0:
        return "N/A"

    url = (
        "https://api.openweathermap.org/data/3.0/onecall/timemachine"
        f"?lat={LAT}&lon={LON}&dt={int(dt.timestamp())}&appid={API_KEY}&units=metric"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data["current"]["temp"]  # Celsius
    except Exception as e:
        print(f"Failed to fetch temperature for {dt} (timestamp={timestamp}): {e}")
        return "N/A"

def main():
    input_file = "data_receive/rad_off_data_corrected.json"
    output_file = "data_receive/rad_off_data_corrected2.csv"

    with open(input_file, "r") as jf:
        data = json.load(jf)

    with open(output_file, "w", newline="") as cf:
        writer = csv.writer(cf)
        
        # CSV header
        writer.writerow(["timestamp", "sensor_id", "humidity", "temperature (sensor reading)", "temperature (outdoor)"])

        for record in data:
            ts = record.get("timestamp")
            sid = record.get("sensor_id", "")
            hum = record.get("dht22_humidity", "")
            temp_sensor = record.get("temperature", "")

            if ts:
                temp_outdoor = get_outdoor_temp_utc(ts)
            else:
                temp_outdoor = ""

            # convert Unix timestamp to human-readable format
            formatted_ts = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([formatted_ts, sid, hum, temp_sensor, temp_outdoor])

    print(f"CSV file generated: {output_file}")

if __name__ == "__main__":
    main()