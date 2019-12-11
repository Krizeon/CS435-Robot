from machine import Pin, UART
import utime

def get_distance():
""" 
Gets and returns distance in cm from US-100 Ultra Sonice Distance Sensor
"""

    # initalize uart instance
    uart = UART(1, 9600)
    uart.init(9600, bits=8, parity=None, stop=1, tx=17, rx=16)

    # initalize buffers used for data tx
    write_buf = bytearray(1)
    write_buf[0] = 0x55
    read_buf = bytearray(2)

    # write 0x55 to tx to initiate UART data tx
    uart.write(write_buf)
    
    # when no sleep, found that it would return 0 - possibly due to speed of sonar?
    utime.sleep_ms(20)
    
    # read 2 bytes returned from UART, MSB first
    uart.readinto(read_buf)
    
    # calculate actual distance per instructions shown on data page 
    distance = read_buf[0] * 256 + read_buf[1]
    return distance




