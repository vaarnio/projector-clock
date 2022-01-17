from machine import Pin, mem16
import uasyncio
import time

async def common(pin, offset):
    print("com task started")
    i = 0
    await uasyncio.sleep_ms(offset)
    while(True):
        com1 = Pin(pin, Pin.OUT)
        com1.value(i%2)
        i += 1
        await uasyncio.sleep_ms(8)
        com1 = Pin(pin, Pin.IN)
        await uasyncio.sleep_ms(8)

def run2():
    print("lcd task started")
    #com1task = uasyncio.create_task(common(32, 0))
    #com2task = uasyncio.create_task(common(33, 8))
    loop = uasyncio.get_event_loop()
    loop.create_task(common(32, 0))
    loop.create_task(common(33, 0))
    loop.run_forever()

@micropython.viper
def set_gpio_out(value:int, mask:int):
    GPIO_OUT = ptr32(0x3FF44004) # GPIO Output register
    GPIO_OUT[0] = (GPIO_OUT[0] & mask) | value

async def runCommon():
    print("com task started")
    #i = 0
    while(True):
        #i += 1
        set_gpio_out(0b00000000000000000100000000000000,
                     0b11111111111111111010111111111111)
        #await uasyncio.sleep_ms(8)
        #set_gpio_in (0b00000000000000000101000000000000,
        #             0b11111111111111111010111111111111)
        await uasyncio.sleep_ms(8)
        set_gpio_out(0b00000000000000000001000000000000,
                     0b11111111111111111010111111111111)
        await uasyncio.sleep_ms(8)

def run():
    loop = uasyncio.get_event_loop()
    loop.create_task(runCommon())
    loop.run_forever()
