import RPi.GPIO as GPIO

LED_PIN = 23

class Heater(object):
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)

    def set_led(self, value):
        ''' Turn led on or off '''
        GPIO.output(LED_PIN, value)

    def get_status(self):
        ''' Get led status if on or off '''
        return GPIO.input(LED_PIN)