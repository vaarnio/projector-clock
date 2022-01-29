from machine import Pin, mem16
import uasyncio
import time

@micropython.viper
def set_gpio_out(value:int, mask:int):
    GPIO_OUT = ptr32(0x3FF44004) # GPIO Output register
    GPIO_OUT[0] = (GPIO_OUT[0] & mask) | value

@micropython.viper
def set_gpio_in(value:int, mask:int):
    GPIO_FUNC_18_OUT_SEL_CFG = ptr32(0x3FF44530+0x4*18)
    GPIO_FUNC_19_OUT_SEL_CFG = ptr32(0x3FF44530+0x4*19)
    GPIO_ENABLE = ptr32(0x3FF44020)
    IO_MUX_18 = ptr32(0x3FF49070)
    IO_MUX_19 = ptr32(0x3FF49074)

    GPIO_FUNC_18_OUT_SEL_CFG[10] = 1
    GPIO_FUNC_19_OUT_SEL_CFG[10] = 0
    GPIO_ENABLE[18] = 1
    GPIO_ENABLE[19] = 0
    IO_MUX_18[13] = 1 #MCU_SEL to 0b010
    IO_MUX_19[13] = 1
    IO_MUX_18[9] = 0  #FUN_IE
    IO_MUX_19[9] = 1
    IO_MUX_18[8] = 1  #pullup
    IO_MUX_19[8] = 0
    IO_MUX_18[7] = 0  #pulldown disable
    IO_MUX_19[7] = 0

async def runSegment():
    print("seg task started")

    Pin

    #initialize pins, otherwise set_gpio_out won't work
    set_gpio_out(0b00000000000000000000000000000000,
                 0b11111111111111111111111111111111)

async def runCommon():
    print("com task started")

    i = 0
    while(True):
        i += 1
        Pin(18, Pin.OUT).value(i % 2)
        Pin(19, Pin.IN)
        await uasyncio.sleep_ms(8)
        Pin(18, Pin.IN)
        Pin(19, Pin.OUT).value(i % 2)
        await uasyncio.sleep_ms(8)

def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(runCommon())
    loop.run_forever()
