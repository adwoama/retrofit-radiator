# micropython code for BME 280
'''
This code reads the temperature, pressure and humidity from the BME280 sensor 
and prints the values to the console.

On PyPi you will install "micropython-bme280" library.

References:
- https://electrocredible.com/raspberry-pi-pico-bme280-interfacing-guide-using-micropython/
- https://microcontrollerslab.com/bme280-raspberry-pi-pico-micropython-tutorial/
'''

from time import sleep, ticks_ms, ticks_diff
import utime
import csv
from sensors import read_dht_sensor, read_bme_sensor
from mpc import run_mpc
from datastream import send_data_to_mqtt, connect_wifi, sync_time, send_fan_state


# Constants
MEASUREMENT_INTERVAL = 300000  # 5 minutes in milliseconds
set_back = 4 #degrees Celcius
set_point = 24 #degrees Celcius

schedule = []

def load_schedule(filepath):
    """
    Loads the schedule from a CSV file.
    """
    global schedule
    with open(filepath, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            schedule.append({
                "unix_time": int(row["Unix Time"]),
                "eastern_time": row["Eastern Time"],
                "occupancy": int(row["Occupancy"])
            })

def is_room_occupied(current_time):
    """
    Determines if the room is occupied based on the current Unix time.
    """
    for entry in schedule:
        if current_time < entry["unix_time"]:
            return entry["occupancy"]
    return 0  # Default to unoccupied if no matching entry is found

def control_fan(temperature):
    """
    Controls the fan based on the temperature reading and occupancy status.
    """
    current_time = utime.time()
    occupied = is_room_occupied(current_time)

    target_temperature = set_point if occupied else set_point - set_back

    if temperature < target_temperature:
        print("Turning fan ON to raise temperature")
        send_fan_state("on")
    else:
        print("Turning fan OFF to lower temperature")
        send_fan_state("off")

# Variables
last_measurement_time = ticks_ms()

# Load the schedule
load_schedule("/lib/schedule.csv")

connect_wifi()
sync_time()


#Measure once before looping
timestamp = utime.time()


temperature, humidity = read_dht_sensor(2)
data = {
    "sensor_id": "room",
    "timestamp": timestamp,
    "temperature": temperature,
    "bme_humidity": humidity,
    "pressure": pressure,
}
print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
send_data_to_mqtt(data)
control_fan(temperature)

#measure every 5 minutes
while True:
    current_time = ticks_ms()

    # Check if it's time to read the sensors
    if ticks_diff(current_time, last_measurement_time) >= MEASUREMENT_INTERVAL:
        # Read data from DHT sensor
        temperature, pressure, humidity = read_bme_sensor(5,4)
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
            # Send data to PC
            timestamp = utime.time()
            #Sensor 1
            data = {
                "sensor_id": "room1",
                "timestamp": timestamp,
                "temperature": temperature,
                "dht22_humidity": humidity,
            }
            send_data_to_mqtt(data)
            control_fan(temperature)
            
        else:
            print("Failed to read sensor 1 data.")
        
        
        # Update the last measurement time
        last_measurement_time = current_time

    # Run the model predictive control logic
    # TODO mpc_result = run_mpc()
    #TODO print(f"MPC Result: {mpc_result}")

    # Sleep for a short time to avoid busy-waiting
    sleep(1)
