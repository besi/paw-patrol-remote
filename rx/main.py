# Receiver interface @ xec

import network
from esp import espnow
import time
import math
import machine
import neopixel

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
    time.sleep(0.5)


mode_button.irq(trigger=machine.Pin.IRQ_RISING, handler=mode_changed)

colors = [
    (0,0,255),(0,255,0),(128,128,0),(255,20,147),(255,69,0),(0,206,209),(255,0, 0)]

while True:
    host, msg = e.irecv()
    if msg:
        value = int(msg[0])
        for x in range(0,7):
            print(str(int(math.pow(2,x)))+ ' & ' + str(value) + ' = ' + str(value & int(math.pow(2,x))))
            np[x] = (0,0,0)
            if value & int(math.pow(2,x)):
                np[x] = colors[x]
            np.write()
