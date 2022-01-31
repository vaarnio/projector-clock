from machine import Pin, mem16
import uasyncio
import time

@micropython.viper
def set_gpio_out(value:int, mask:int):
    GPIO_OUT = ptr32(0x3FF44004) # GPIO Output register
    GPIO_OUT[0] = (GPIO_OUT[0] & mask) | value

def initPins():
    Pin(32, Pin.OUT).value(0)
    Pin(33, Pin.OUT).value(0)

    Pin(12, Pin.OUT).value(0)
    Pin(13, Pin.OUT).value(0)
    Pin(14, Pin.OUT).value(0)
    Pin(15, Pin.OUT).value(0)
    Pin(16, Pin.OUT).value(0)
    Pin(17, Pin.OUT).value(0)
    Pin(18, Pin.OUT).value(0)

    Pin(19, Pin.OUT).value(0)
    Pin(21, Pin.OUT).value(0)
    Pin(22, Pin.OUT).value(0)
    Pin(23, Pin.OUT).value(0)
    Pin(25, Pin.OUT).value(0)
    Pin(26, Pin.OUT).value(0)
    Pin(27, Pin.OUT).value(0)

com1 = 0b11111111111111111111111111111111
com2 = 0b11111111111111111111111111111111

def com1Digit(digit, value):
    global com1
    digits = [
        { #digit 0
            1: 0b00001000000000000000000000000000,
            2: 0b00000000000000000000000000000000
        },
    ]
    com1 = com1 ^ digits[digit][value]

def com2Digit(digit, value):
    global com2
    digits = [
        { #digit 0
            1: 0b00000100000000000000000000000000,
            2: 0b00001100000000000000000000000000
        },
    ]
    com2 = com2 ^ digits[digit][value]

def setDigit(digit, value):
    com1Digit(digit, value)
    com2Digit(digit, value)

async def runCommon():
    print("com task started")

    initPins()
    global com1
    global com2
    setDigit(0, 2)

    enabled = 0b11111111111111111111111111111111
    mask    = 0b11110011111111100111111111111111 

    i = 0
    while(True):
        i += 1

        enabled = ~ enabled
        set_gpio_out(enabled | com1, mask)

        Pin(32, Pin.OUT).value(1)
        Pin(33, Pin.IN)
        await uasyncio.sleep_ms(8)

        set_gpio_out(enabled | com2, mask)

        Pin(32, Pin.IN)
        Pin(33, Pin.OUT).value(1)
        await uasyncio.sleep_ms(8)

        enabled = ~ enabled
        set_gpio_out(enabled ^ com1, mask)

        Pin(32, Pin.OUT).value(0)
        Pin(33, Pin.IN)
        await uasyncio.sleep_ms(8)

        set_gpio_out(enabled ^ com2, mask)

        Pin(32, Pin.IN)
        Pin(33, Pin.OUT).value(0)
        await uasyncio.sleep_ms(8)

def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(runCommon())
    #loop.create_task(runSegment())
    loop.run_forever()
