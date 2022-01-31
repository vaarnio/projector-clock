import lcd
import socket
import network
import ntptime
import time

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

TIMEZONE_DIFFERENCE = 1
dst_on = False

def resolve_dst_and_set_time():
    global TIMEZONE_DIFFERENCE
    global dst_on
    # This is most stupid thing what humans can do!
    # Rules for Finland: DST ON: March last Sunday at 03:00 + 1h, DST OFF: October last Sunday at 04:00 - 1h
    # Sets localtime to DST localtime
    if network.WLAN(network.STA_IF).config('essid') == '':
        now = time.mktime(time.localtime())
        if DEBUG_ENABLED == 1:
            print("Network down! Can not set time from NTP!")
    else:
        now = ntptime.time()

    (year, month, mdate, hour, minute, second, wday, yday) = time.localtime(now)

    if year < 2020:
        if DEBUG_ENABLED == 1:
            print("Time not set correctly!")
        return False

    dstend = time.mktime((year, 10, (31 - (int(5 * year / 4 + 1)) % 7), 4, 0, 0, 0, 6, 0))
    dstbegin = time.mktime((year, 3, (31 - (int(5 * year / 4 + 4)) % 7), 3, 0, 0, 0, 6, 0))

    if TIMEZONE_DIFFERENCE >= 0:
        if (now > dstbegin) and (now < dstend):
            dst_on = True
            ntptime.NTP_DELTA = 3155673600 - ((TIMEZONE_DIFFERENCE + 1) * 3600)
        else:
            dst_on = False
            ntptime.NTP_DELTA = 3155673600 - (TIMEZONE_DIFFERENCE * 3600)
    else:
        if (now > dstend) and (now < dstbegin):
            dst_on = False
            ntptime.NTP_DELTA = 3155673600 - (TIMEZONE_DIFFERENCE * 3600)
        else:
            dst_on = True
            ntptime.NTP_DELTA = 3155673600 - ((TIMEZONE_DIFFERENCE + 1) * 3600)
    if dst_on is None:
        if DEBUG_ENABLED == 1:
            print("DST calculation failed!")
            return False
    else:
        ntptime.settime()

def run():
    do_connect()
    resolve_dst_and_set_time()
    print(time.localtime())
    #print(get_time())
    lcd.run()