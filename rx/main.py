# Receiver interface @ xec

import network
from esp import espnow
import time
import math
import machine
import neopixel
import struct
import uasyncio

ALL_SWITCHES = 127

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)
w0.active(True)
e = espnow.ESPNow()
e.init()

print("Starting receiver...")
print("".join("%02x:" % i for i in w0.config('mac'))[0:-1])
peer = b"\xd8\xa0\x1d]\xcc\xb8"
e.add_peer(peer)

np = neopixel.NeoPixel(machine.Pin(4), 7)

def clear():
    np.fill((0, 0, 0))
    np.write()


def pretty():
    global np
    np[0] = (6 * 36, 7 * 36, 4 * 36)
    np[1] = (2 * 36, 7 * 36, 5 * 36)
    np[2] = (3 * 36, 4 * 36, 1 * 36)
    np[3] = (1 * 36, 2 * 36, 7 * 36)
    np[4] = (4 * 36, 2 * 36, 5 * 36)
    np[5] = (1 * 36, 7 * 36, 1 * 36)
    np[6] = (7 * 36, 3 * 36, 1 * 36)

    np.write()

pretty()

mode = 0
modes = 6
mode_pin = 26
mode_button = machine.Pin(mode_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)

def mode_changed(event):
    global mode, modes
    mode = mode + 1
    mode = mode % (modes + 1)
    if mode == 1:
        pretty()
    elif mode == 2:
        np.fill((255, 255, 255))
    elif mode == 3:
        np.fill((0, 0, 255))
    elif mode == 4:
        np.fill((255, 0, 0))
    elif mode == 5:
        np.fill((0, 255, 0))
    elif mode == 6:
        clear()
    np.write()
    time.sleep(1)


async def rainbow():
    # Rainbow code by https://wokwi.com/arduino/projects/305569065545499202

    rainbow = [
      (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
      (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
      (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
      (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

    while True:
        rainbow = rainbow[-1:] + rainbow[:-1]
        for i in range(7):
            np[i] = rainbow[i]
            np.write()
        
        await uasyncio.sleep_ms(100)

mode_button.irq(trigger=machine.Pin.IRQ_RISING, handler=mode_changed)

colors = [
    (0,0,255),(0,255,0),(128,128,0),(255,20,147),(255,69,0),(0,206,209),(255,0, 0)]
   
   
t = None
msg = None

async def areadespnow(s,t):
    global msg
    while True:
        msg = await(s.read(-1))
        
        print(f"msg {msg}")        
        t.cancel()
        break;
        
s = uasyncio.StreamReader(e)

def update_pixels(value):
    for x in range(0,7):
            np[x] = (0,0,0)
            if value & int(math.pow(2,x)):
                np[x] = colors[x]
            np.write()    

while True:
    host, msg = e.irecv()
    if msg:
        value = int(msg[0])
        print(value)
        if value == ALL_SWITCHES:
            update_pixels(value)
            time.sleep(.5)
            event_loop = uasyncio.get_event_loop()
            t = event_loop.create_task(rainbow())
            et = event_loop.create_task(areadespnow(s,t))
            event_loop.run_forever()
            value=struct.unpack('<8sH',msg)[1]
            
        
        update_pixels(value)
