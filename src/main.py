import clock
import lcd
import uasyncio
import network

def do_connect():
    wifiFile = open('./secret/wifi', 'r')
    wifi = wifiFile.read().split('\n')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi[0], wifi[1])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def run():
    do_connect()
    clock.resolve_dst_and_set_time()
    clock.run()
    #print(get_time())
    #l = lcd.Lcd()
    #loop = uasyncio.get_event_loop()
    #loop.create_task(l.runCommon())
    #loop.create_task(clock.runClock())

run()