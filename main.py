# micropython code for BME 280
'''
This code reads the temperature, pressure and humidity from the BME280 sensor 
and prints the values to the console.

On PyPi you will install "micropython-bme280" library.

References:
- https://electrocredible.com/raspberry-pi-pico-bme280-interfacing-guide-using-micropython/
- https://microcontrollerslab.com/bme280-raspberry-pi-pico-micropython-tutorial/
'''

from time import sleep
import machine
import BME280

import network
from umqtt.simple import MQTTClient

sdaPin1 = machine.Pin(2)
sclPin1 = machine.Pin(3)

i2c1 = machine.I2C(sda=sdaPin1, scl=sclPin1, freq=400000)
bme1 = bme280.BME280(i2c=i2c1)

while True:
    time.sleep(10) # sleep for 10 seconds
    t, p, h = bme1.read_compensated_data()
    
    temp1 = t/100
    p = p//256 # convert to hPa
    pressure1 = p//100

    hi = h//1024
    hd = h*100 // 1024 = hi * 100
    print("Temperature: ", temp1, "C")
    print("Pressure: ", pressure1, "hPa")
    print("Humidity: ", hi, "%")
    print("Humidity: ", hd, "%")
    print("\n")