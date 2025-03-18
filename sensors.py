#functions to read from the DHT22 and BME280 sensors

from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff
import dht
from bme280 import BME280  # Ensure you have the MicroPython BME280 library installed



def read_dht_sensor(pin):
    """
    Reads the DHT22 sensor and returns temperature and humidity as decimals.
    """
    dht_sensor = dht.DHT22(machine.Pin(pin))
    try:
        dht_sensor.measure()
        temperature = float(dht_sensor.temperature())
        humidity = float(dht_sensor.humidity())
        return temperature, humidity
    except Exception as e:
        print(f"Error reading DHT sensor: {e}")
        return None, None
    

def read_bme_sensor(scl_pin, sda_pin):
    """
    Reads the BME280 sensor and returns temperature, pressure, and humidity as decimals.
    
    Parameters:
        scl_pin (int): The GPIO pin for the I2C clock (SCL).
        sda_pin (int): The GPIO pin for the I2C data line (SDA).
    
    Returns:
        tuple: Temperature, pressure, and humidity as floats, or (None, None, None) if an error occurs.
    """
    try:
        # Initialize I2C with the given pins
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        bme = BME280(i2c=i2c)
        
        # Read data from the BME280 sensor
        temperature = float(bme.temperature[:-1])  # Remove the 'C' at the end
        pressure = float(bme.pressure[:-3])  # Remove the 'hPa' at the end
        humidity = float(bme.humidity[:-1])  # Remove the '%' at the end
        
        return temperature, pressure, humidity
    except Exception as e:
        print(f"Error reading BME280 sensor: {e}")
        return None, None, None