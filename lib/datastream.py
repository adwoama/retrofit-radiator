#functions to stream data from RPi pico W to our PC

import utime
import network
import ujson
import socket
import ntptime

from umqtt.simple import MQTTClient

from wifi_config import WIFI_SSID, WIFI_PASSWORD

BROKER = "test.mosquitto.org"  # Free public broker
PORT = 1883
TOPIC = "cmu/retrofit_radiator/sensor1"
TOPIC_FAN_STATE = b"cmu/retrofit_radiator/fan_state"  # Topic to control the fan state



def sync_time():
    """
    Synchronize the Pico W's time with an NTP server.
    """
    try:
        print("Synchronizing time with NTP server...")
        ntptime.settime()  # Synchronize time using the default NTP server
        print("Time synchronized!")
    except Exception as e:
        print(f"Failed to synchronize time: {e}")

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

def send_fan_state(state):
    """
    Sends the fan state ('on' or 'off') to the MQTT broker.
    """
    try:
        # Initialize MQTT client
        client = MQTTClient("pico_w_client", BROKER, PORT)
        client.connect()
        print(f"Connected to MQTT broker at {BROKER}")

        # Publish the fan state to the topic
        client.publish(TOPIC_FAN_STATE, state.encode())
        print(f"Sent '{state}' to topic '{TOPIC_FAN_STATE.decode()}'")

        # Disconnect from the broker
        client.disconnect()
    except Exception as e:
        print(f"Error: {e}")
    
    
    
