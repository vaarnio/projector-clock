import lcd
import socket
import network
import ntptime
import time
import uasyncio

TIMEZONE_DIFFERENCE = 2
dst_on = None

def resolve_dst_and_set_time():
    global TIMEZONE_DIFFERENCE
    global dst_on
    # Rules for Finland: DST ON: March last Sunday at 03:00 + 1h, DST OFF: October last Sunday at 04:00 - 1h
    # Sets localtime to DST localtime
    if network.WLAN(network.STA_IF).config('essid') == '':
        now = time.mktime(time.localtime())
        if DEBUG_ENABLED == 1:
            print("Network down! Can not set time from NTP!")
    else:
        now = ntptime.time()

    (year, month, mdate, hour, minute, second, wday, yday) = time.localtime(now)

    if year < 2022:
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
        print(time.localtime())

def zfl(s, width):
    # Pads the provided string with leading 0's to suit the specified 'chrs' length
    # Force # characters, fill with leading 0's
    return '{:0>{w}}'.format(s, w=width)

async def setTime(l):
    lastMinute = 0
    lastSetTime = 0
    while(True):
        (year, month, mdate, hour, minute, second, wday, yday) = time.localtime()
        if(minute != lastMinute):
            timeStr = zfl(hour, 2) + zfl(minute, 2)
            l.setOutput(timeStr)
        if(hour == 0 and lastSetTime != time.time()):
            resolve_dst_and_set_time()
            lastSetTime = time.time()
        await uasyncio.sleep_ms(1000)

def run():
    l = lcd.Lcd()
    loop = uasyncio.get_event_loop()
    loop.create_task(l.runCommon())
    loop.create_task(setTime(l))
    loop.run_forever()