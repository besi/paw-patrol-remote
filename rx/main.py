# Receiver interface @ xec

import network
from esp import espnow
import time
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
    np[0] = (1 * 36, 2 * 36, 7 * 36)
    np[1] = (2 * 36, 7 * 36, 7 * 36)
    np[2] = (3 * 36, 1 * 36, 4 * 36)
    np[3] = (4 * 36, 2 * 36, 5 * 36)
    np[4] = (1 * 36, 3 * 36, 6 * 36)
    np[5] = (6 * 36, 4 * 36, 2 * 36)
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

while True:
    host, msg = e.irecv()
    if msg:
        # msg == None if timeout in irecv()
        print(host, msg)
        if msg == b"green":
            np.fill((0, 255, 0))
        if msg == b"red":
            np.fill((255, 0, 0))
        if msg == b"blue":
            np.fill((0, 0, 255))
        if msg == b"white":
            np.fill((255, 255, 255))
        if msg == b"orange":
            np.fill((128, 128, 0))
        if msg == b"purple":
            np.fill((128, 0, 128))
        if msg == b"off":
            np.fill((0, 0, 0))
        if msg == b"reset":
            pretty()
        if msg == b"end":
            break
        np.write()
