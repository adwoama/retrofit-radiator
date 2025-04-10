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
from sensors import read_dht_sensor, read_bme_sensor
from mpc import run_mpc
from datastream import send_data_to_mqtt, connect_wifi, sync_time
from fan import fanOn, fanOff

# Constants
MEASUREMENT_INTERVAL = 600000  # 10 minutes in milliseconds
server_url = "https://abcd1234.ngrok.io/receive-data" #TODO placeholder url

# Variables
last_measurement_time = ticks_ms()

connect_wifi()
sync_time()
fanOn()

#Measure once before looping
timestamp = utime.time()
temperature, pressure, humidity = read_bme_sensor(5,4)
data = {
    "sensor_id": "room1",
    "timestamp": timestamp,
    "temperature": temperature,
    "bme_humidity": humidity,
    "pressure": pressure,
}
send_data_to_mqtt(data)
print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

temperature, pressure, humidity = read_bme_sensor(7,6)
data = {
    "sensor_id": "room2",
    "timestamp": timestamp,
    "temperature": temperature,
    "bme_humidity": humidity,
    "pressure": pressure,
}
print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Pressure: {pressure}hPa")
send_data_to_mqtt(data)

#measure every 10 minutes
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

            
        else:
            print("Failed to read sensor 1 data.")
        
        #Sensor 2
        temperature, pressure, humidity = read_bme_sensor(7,6)
        if temperature is not None and humidity is not None:
            data = {
                "sensor_id": "room2",
                "timestamp": timestamp,
                "temperature": temperature,
                "bme_humidity": humidity,
                "pressure": pressure,
            }
            send_data_to_mqtt(data)
        else:
            print("Failed to read sensor 2 data.")
        # Update the last measurement time
        last_measurement_time = current_time

    # Run the model predictive control logic
    # TODO mpc_result = run_mpc()
    #TODO print(f"MPC Result: {mpc_result}")

    # Sleep for a short time to avoid busy-waiting
    sleep(1)
