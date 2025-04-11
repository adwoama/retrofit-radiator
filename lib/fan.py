from machine import Pin, PWM
import time

# Define PWM pin for fan control
#fan_pwm = PWM(Pin(15))  # Connect to the PWM wire of the fan
#fan_pwm.freq(25000)     # Set PWM frequency to 25kHz

relay = Pin(16, Pin.OUT) # The pin that is connected to the Input Circuit of the Relay

#while True:  # Loop forever
    #relay.value(0)  # Turn the relay ON
    #time.sleep(1)
    #relay.value(1)  # Turn the relay OFF
    #time.sleep(1)

def fanOn():
    """Turns the fan ON at full speed."""
    #fan_pwm.duty_u16(65535)  # 100% duty cycle
    relay.value(0)

def fanOff():
    """Turns the fan OFF."""
    #fan_pwm.duty_u16(0)  # 0% duty cycle
    relay.value(1)

def setFanSpeed(percent):
    """Sets fan speed as a percentage (0-100%)."""
    duty = int((percent / 100) * 65535)  # Scale 0-100% to 16-bit PWM
    fan_pwm.duty_u16(duty)


