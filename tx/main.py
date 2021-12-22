# transmitter interface 145320 @ xb8

import machine
from time import sleep
import math
import network
from esp import espnow
from struct import pack

ON = 0
OFF = 1

# Setup LEDs
led_pins = [17, 16, 4, 0, 2, 15, 13]
leds = list(map(lambda x: machine.Pin(x, machine.Pin.OUT), led_pins))

# Setup switches
switch_pins = [35,34,22,19,23,18, 5]
def make_switch(pin):
    switch = machine.Pin(pin, machine.Pin.IN)
    return switch
switches = list(map(make_switch, switch_pins))

def animate(leds):    
    for led in leds:
        led.value(1)
        sleep(.05)
    for led in leds:
        led.value(0)
        sleep(.05)
    for led in leds:
        led.value(1)
        sleep(.05)

animate(leds)

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)  # Or network.AP_IF
w0.active(True)
now = espnow.ESPNow()
now.init()

print("Starting transmitter...")
print("".join("%02x:" % i for i in w0.config('mac'))[0:-1])
peer = b'\x94\xb9~\xe5B\xec'
now.add_peer(peer)


current_value = 0
last_value = 0
while True:
    current_value = 0
    for switch in switches:
        index = switches.index(switch)
        led = leds[index]
        led.value(switch.value())
        if switch.value() == ON:
            current_value = current_value + int(math.pow(2, index))
    
    if current_value != last_value:
        now.send(peer, pack('h', current_value), True)
        print(f"Sending {current_value}")
    last_value = current_value
    sleep(0.25)




# 
now.send(b'red')
