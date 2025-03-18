#functions to stream data from RPi pico W to our PC

from wifi_config import WIFI_SSID, WIFI_PASSWORD

def send_data_to_pc(data):
    """
    Sends data to the PC remotely.
    """
    print(f"Connecting to Wi-Fi SSID: {WIFI_SSID}")
    print(f"Sending data to PC: {data}")
    # Add your data streaming logic here