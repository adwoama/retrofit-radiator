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

# Constants
MEASUREMENT_INTERVAL = 600000  # 10 minutes in milliseconds
server_url = "https://abcd1234.ngrok.io/receive-data" #TODO placeholder url

# Variables
last_measurement_time = ticks_ms()

connect_wifi()
sync_time()

#Measure once before looping
timestamp = utime.time()
temperature, humidity = read_dht_sensor(2)
data = {
    "sensor_id": "radiator",
    "timestamp": timestamp,
    "temperature": temperature,
    "dht22_humidity": humidity,
}
send_data_to_mqtt(data)
print(f"Temperature: {temperature}°C, Humidity: {humidity}%")



#measure every 10 minutes
while True:
    current_time = ticks_ms()

    # Check if it's time to read the sensors
    if ticks_diff(current_time, last_measurement_time) >= MEASUREMENT_INTERVAL:
        # Read data from DHT sensor
        temperature, humidity = read_dht_sensor(2)
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
            # Send data to PC
            timestamp = utime.time()
            #Radiator Sensor
            data = {
                "sensor_id": "radiator",
                "timestamp": timestamp,
                "temperature": temperature,
                "dht22_humidity": humidity,
            }
            send_data_to_mqtt(data)

           
        else:
            print("Failed to read sensor data.")
        
        # Update the last measurement time
        last_measurement_time = current_time

    # Run the model predictive control logic
    # TODO mpc_result = run_mpc()
    #TODO print(f"MPC Result: {mpc_result}")

    # Sleep for a short time to avoid busy-waiting
    sleep(1)
