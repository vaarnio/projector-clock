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
            0: 0b00000000000000000000000000000000,
            1: 0b00001000000000000000000000000000,
            2: 0b00000000000000000000000000000000
        },
        { #digit 1
            0: 0b00000010110000000000000000000000,
            1: 0b00000000010000000000000000000000,
            2: 0b00000010101000000000000000000000,
            3: 0b00000000111000000000000000000000,
            4: 0b00000000011000000000000000000000,
            5: 0b00000000111000000000000000000000,
            6: 0b00000010111000000000000000000000,
            7: 0b00000000010000000000000000000000,
            8: 0b00000010111000000000000000000000,
            9: 0b00000000111000000000000000000000,
        },
        { #digit 2              5
            0: 0b00000000000001010000000000000000,
            1: 0b00000000000000010000000000000000,
            2: 0b00000000000001100000000000000000,
            3: 0b00000000000000110000000000000000,
            4: 0b00000000000000110000000000000000,
            5: 0b00000000000000110000000000000000,
        },
        { #digit 3                 2
            0: 0b00000000000000001110000000000000,
            1: 0b00000000000000000010000000000000,
            2: 0b00000000000000001101000000000000,
            3: 0b00000000000000000111000000000000,
            4: 0b00000000000000000011000000000000,
            5: 0b00000000000000000111000000000000,
            6: 0b00000000000000001111000000000000,
            7: 0b00000000000000000010000000000000,
            8: 0b00000000000000001111000000000000,
            9: 0b00000000000000000111000000000000,
        }
    ]
    com1 = com1 ^ digits[digit][value]

def com2Digit(digit, value):
    global com2
    digits = [
        { #digit 0
            0: 0b00000000000000000000000000000000,
            1: 0b00000100000000000000000000000000,
            2: 0b00001100000000000000000000000000
        },
        { #digit 1
            0: 0b00000010011000000000000000000000,
            1: 0b00000000010000000000000000000000,
            2: 0b00000000011000000000000000000000,
            3: 0b00000000011000000000000000000000,
            4: 0b00000010010000000000000000000000,
            5: 0b00000010001000000000000000000000,
            6: 0b00000010001000000000000000000000,
            7: 0b00000000011000000000000000000000,
            8: 0b00000010011000000000000000000000,
            9: 0b00000010011000000000000000000000,
        },
        { #digit 2              5
            0: 0b00000000000001110000000000000000,
            1: 0b00000000000000010000000000000000,
            2: 0b00000000000000110000000000000000,
            3: 0b00000000000000110000000000000000,
            4: 0b00000000000001010000000000000000,
            5: 0b00000000000001100000000000000000,
        },
        { #digit 3                 2
            0: 0b00000000000000001011000000000000,
            1: 0b00000000000000000010000000000000,
            2: 0b00000000000000000011000000000000,
            3: 0b00000000000000000011000000000000,
            4: 0b00000000000000001010000000000000,
            5: 0b00000000000000001001000000000000,
            6: 0b00000000000000001001000000000000,
            7: 0b00000000000000000011000000000000,
            8: 0b00000000000000001011000000000000,
            9: 0b00000000000000001011000000000000,
        }
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

    enabled =  0b11111111111111111111111111111111
    mask    =  0b11110000000000000000111111111111

    while(True):
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

async def runClock():
    global com1
    global com2
    i = 0
    while(True):
        com1 = 0b11111111111111111111111111111111
        com2 = 0b11111111111111111111111111111111

        if(i > 9):
            i = 0

        setDigit(0, 2)
        setDigit(1, 3)
        setDigit(2, 5)
        setDigit(3, 9)

        i += 1
        await uasyncio.sleep_ms(1000)

def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(runCommon())
    loop.create_task(runClock())
    loop.run_forever()
