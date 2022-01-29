import time
from machine import Pin
led=Pin(14,Pin.OUT)

def blink():
    while True:
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)