import network
import utime
from machine import Pin, PWM

def load_cred():
    """
    Load credentials from file
    No encryption, it is quite difficult to encrypt
    in this scenario since the key has to be somewhere
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

    # You can (and should) change the IP address to avoid conflict with others
    #
    # ap_if.ifconfig((IP, subnet_mask, gateway, dns))
    ap_if.ifconfig(('4.3.5.2', '255.255.255.0', '4.3.5.2', '4.3.5.2'))
    #
    # IP          is your desired IP address (we could use 4.3.5.host) where host is a number between 1-254
    # subnet_mask is used to split the IP range. Typical value for us 255.255.255.0
    #             meaning that the first 3 bytes define the network and the last, the indivitual hosts
    # gateway     is the address of the "router" connected to the web. In our case the ESP32 so it should be
    #             the same as the IP
    # dns         is the domain name service address. The computer that does the translation between hostnames
    #             (www.google.com) and IP addresses (172.217.6.228). We don't have one so you can use the IP
    #             address

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
