# transmitter interface 145320 @ xb8

import machine
import network
from esp import espnow
from time import sleep

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)  # Or network.AP_IF
w0.active(True)
now = espnow.ESPNow()
now.init()

print("Starting transmitter...")
print("".join("%02x:" % i for i in w0.config('mac'))[0:-1])
peer = b'\x94\xb9~\xe5B\xec'   # MAC address of peer's wifi interface
now.add_peer(peer)

led_pins = [17, 16, 4, 0, 2, 15, 13]
switch_pins = [35,34,22,19,23,18, 5]

leds = []

for p in led_pins:
    l = machine.Pin(p, machine.Pin.OUT)
    l.value(1)


green_pin = 35
red_pin = 34
blue_pin = 22
white_pin = 19
purple_pin = 23
orange_pin = 18
off_pin = 5

green = machine.Pin(green_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
red = machine.Pin(red_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
blue = machine.Pin(blue_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
white = machine.Pin(white_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
purple = machine.Pin(purple_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
orange = machine.Pin(orange_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
off = machine.Pin(off_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)

now.send("Starting...")       # Send to all peers

while True:
    if green.value() == 1 and red.value() == 1:
        # special rainbow
        now.send(peer, 'reset', True)
        print('reset')
    elif green.value() == 1:
        now.send(peer,'green', True)
        print('green sent')
    elif red.value() == 1:
        now.send(peer,'red', True)
        print('red  sent')
    elif white.value() == 1:
        now.send(peer,'white', True)
    elif blue.value() == 1:
        now.send(peer,'blue', True)
    elif orange.value() == 1:
        now.send(peer,'orange', True)
    elif purple.value() == 1:
        now.send(peer,'purple', True)
    elif off.value() == 1:
        now.send(peer,'off', True)
    sleep(0.2)


now.send(b'end')
