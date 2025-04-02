#functions to stream data from RPi pico W to our PC

import utime
import network
import ujson
import socket
from umqtt.simple import MQTTClient

from wifi_config import WIFI_SSID, WIFI_PASSWORD

BROKER = "test.mosquitto.org"  # Free public broker
PORT = 1883
TOPIC = "cmu/retrofit_radiator/sensor1"

def connect_wifi():
    #connect to wifi
    print(f"Connecting to Wi-Fi SSID: {WIFI_SSID}")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wifi.isconnected():
        utime.sleep(1)

    print("Connected to WiFi!")


def send_data_to_mqtt(data):
    """
    Published data to MQTT broker.
    """
    client = MQTTClient("12770_retrofit_rad", BROKER, port=PORT)
    client.connect()
    print(f"Connected to MQTT broker at {BROKER}")

    payload = ujson.dumps(data)
    client.publish(TOPIC, payload)
    print(f"Published data to topic '{TOPIC}': {payload}")

    client.disconnect()
    
    
    
