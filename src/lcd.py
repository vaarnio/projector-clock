from machine import Pin, mem16
import uasyncio
import time

@micropython.viper
def set_gpio_out(value:int, mask:int):
    GPIO_OUT = ptr32(0x3FF44004) # GPIO Output register
    GPIO_OUT[0] = (GPIO_OUT[0] & mask) | value

class Lcd:
    """"Class responsible for directly driving the lcd"""
    com1 = 0b11111111111111111111111111111111
    com2 = 0b11111111111111111111111111111111

    def __init__(self):
        self.com1 = 0b11111111111111111111111111111111
        self.com2 = 0b11111111111111111111111111111111

        #init pins
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



    def com1Digit(self, digit, value):
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
        self.com1 = self.com1 ^ digits[digit][value]

    def com2Digit(self, digit, value):
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
        self.com2 = self.com2 ^ digits[digit][value]

    def setDigit(self, digit, value):
        value = int(value)
        self.com1Digit(digit, value)
        self.com2Digit(digit, value)

    def setOutput(self, strNum):
        self.com1 = 0b11111111111111111111111111111111
        self.com2 = 0b11111111111101111111111111111111
        self.setDigit(0, strNum[0])
        self.setDigit(1, strNum[1])
        self.setDigit(2, strNum[2])
        self.setDigit(3, strNum[3])

    async def runCommon(self):
        print("com task started")
        enabled =  0b11111111111111111111111111111111
        mask    =  0b11110000000000000000111111111111

        #self.setOutput("1111")

        while(True):
            enabled = ~ enabled
            set_gpio_out(enabled | self.com1, mask)

            Pin(32, Pin.OUT).value(1)
            Pin(33, Pin.IN)
            await uasyncio.sleep_ms(8)

            set_gpio_out(enabled | self.com2, mask)

            Pin(32, Pin.IN)
            Pin(33, Pin.OUT).value(1)
            await uasyncio.sleep_ms(8)

            enabled = ~ enabled
            set_gpio_out(enabled ^ self.com1, mask)

            Pin(32, Pin.OUT).value(0)
            Pin(33, Pin.IN)
            await uasyncio.sleep_ms(8)

            set_gpio_out(enabled ^ self.com2, mask)

            Pin(32, Pin.IN)
            Pin(33, Pin.OUT).value(0)
            await uasyncio.sleep_ms(8)

            