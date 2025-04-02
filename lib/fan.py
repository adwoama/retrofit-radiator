from machine import Pin, PWM
import time

# Define PWM pin for fan control
fan_pwm = PWM(Pin(15))  # Connect to the PWM wire of the fan
fan_pwm.freq(25000)     # Set PWM frequency to 25kHz

def fanOn():
    """Turns the fan ON at full speed."""
    fan_pwm.duty_u16(65535)  # 100% duty cycle

def fanOff():
    """Turns the fan OFF."""
    fan_pwm.duty_u16(0)  # 0% duty cycle

def setFanSpeed(percent):
    """Sets fan speed as a percentage (0-100%)."""
    duty = int((percent / 100) * 65535)  # Scale 0-100% to 16-bit PWM
    fan_pwm.duty_u16(duty)

# Example usage
fanOn()    # Full speed
time.sleep(2)
setFanSpeed(50)  # 50% speed
time.sleep(2)
fanOff()   # Turn off

