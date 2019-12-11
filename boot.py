# boot.py

# Intialize access point for hosting webpage for controlling robot
# Adapted from http://acoptex.com/project/2789/basics-project-076e-esp32-development-board-micropython-web-server-at-acoptexcom/">http://acoptex.com/project/2789/basics-project-076e-esp32-development-board-micropython-web-server-at-acoptexcom/</a></p>


import network
import utime
from machine import Pin, PWM


def load_cred():
    """
    Load credentials from unencrypted file
    Contains the accesspoint name and password ESP32 will use
    """
    f = open('cred_ap.txt', 'r')
    c = f.readlines()
    f.close()
    cred = [r.rstrip() for r in c]
    return cred

def ok():
    """
    PWM off and LED on
    """
    PWM(Pin(13)).deinit()
    Pin(13, Pin.OUT).on()

def trying():
    """
    PWM blinking 10 times a second
    """
    PWM(Pin(13), freq=10, duty=512)

def setup():
    """
    Configure the ESP32 to work as access point
    """
    ap_if = network.WLAN(network.AP_IF)

    print("Configuring AP")
    trying()  # Blink the LED while connecting
    ap_if.active(True)
    cred = load_cred()
    ap_if.config(essid=cred[0], password=cred[1], authmode=network.AUTH_WPA2_PSK)

    # set IP address ESP32 will use to host webpage
    # ap_if.ifconfig((IP, subnet_mask, gateway, dns))
    ap_if.ifconfig(('4.3.5.5', '255.255.255.0', '4.3.5.5', '4.3.5.5'))

    # Wait until connected
    while not ap_if.active():
        print('.', end='')
        utime.sleep(1)

    ok()  # Steady LED
    print('\nConnection successful:', ap_if.ifconfig())

    # Return the IP address
    return ap_if.ifconfig()[0]

# Configure and store IP address
ip_addr = setup()
