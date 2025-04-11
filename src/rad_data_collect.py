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
from umqtt.simple import MQTTClient

# Constants
MEASUREMENT_INTERVAL = 600000  # 10 minutes in milliseconds
BROKER = "test.mosquitto.org"  # MQTT broker
PORT = 1883
TOPIC_FAN_STATE = "cmu/retrofit_radiator/fan_state"
server_url = "https://abcd1234.ngrok.io/receive-data" #TODO placeholder url

# Variables
last_measurement_time = ticks_ms()

# Callback function to handle incoming MQTT messages
def mqtt_callback(topic, msg):
    """
    Callback function triggered when a message is received on a subscribed topic.
    """
    print(f"Received message on topic {topic.decode()}: {msg.decode()}")
    if topic.decode() == TOPIC_FAN_STATE:
        if msg.decode().lower() == "on":
            print("Turning fan ON")
            fanOn()
        elif msg.decode().lower() == "off":
            print("Turning fan OFF")
            fanOff()

connect_wifi()
sync_time()
# Initialize MQTT client
client = MQTTClient("12770_retrofit_rad", BROKER, port=PORT)
client.set_callback(mqtt_callback)
client.connect()
print(f"Connected to MQTT broker at {BROKER}")

# Subscribe to the fan_state topic
client.subscribe(TOPIC_FAN_STATE)
print(f"Subscribed to topic '{TOPIC_FAN_STATE}'")

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
    # Check for incoming MQTT messages
    client.check_msg()

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
