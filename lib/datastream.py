#functions to stream data from RPi pico W to our PC

import utime
import network
import ujson
import socket

from wifi_config import WIFI_SSID, WIFI_PASSWORD

def connect_wifi():
    #connect to wifi
    print(f"Connecting to Wi-Fi SSID: {WIFI_SSID}")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        utime.sleep(1)

    print("Connected to WiFi!")

def get_mac_address():
    wifi = network.WLAN(network.STA_IF)
    return wifi.config('mac')

def print_mac_address():
    wifi = network.WLAN(network.STA_IF)
    # Print the MAC address in a readable format
    print("MAC Address:", ':'.join(f'{b:02x}' for b in wifi.config('mac')))
    return

def send_data_to_pc(data, server_url):
    """
    Sends data to the PC remotely.
    """

    
    print(f"Sending data to PC: {data}")
    # Add your data streaming logic here