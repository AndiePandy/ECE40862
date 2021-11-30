import time, network, ntptime, esp32, machine, socket, sys
from machine import Pin, RTC, TouchPad, Timer, wake_reason, SoftI2C       

################### Functions ###################
# Connect to Internet and print local IP (Lab 3)
def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to', ssid)
    print('IP Address:', wlan.ifconfig()[0])
    print('')
    
# HTTP GET request as described in the micropython documentation
def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
m    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    #while True:
    #    data = s.recv(100)
    #    if data:
    #        print(str(data, 'utf8'), end='')
    #    else:
    #        break
    s.close()
    
def thingspeak_timer(i):
    # read data from Thingspeak
    print("checking thingspeak") # please get rid of
    #http_get("https://api.thingspeak.com/channels/1583988/fields/1.json?api_key=FJVB6CAQ1GB79AKH&results=2") # ERROR with http_get

############## 3.2 Software Init ###################
# Init LEDS, Timers, Interrupts (if needed)        #
# use I2C driver to communicate with Accelerometer #
####################################################
led_red = Pin(21, Pin.OUT)   # Onboard RED LED is connected to IO_21
led_green = Pin(27, Pin.OUT) # Onboard GREEN LED is connected to IO_27
led_red.value(0)             # should be off when init
led_green.value(0)           # should be off when init

timer_thingspeak = Timer(0)

i2c = SoftI2C(scl=Pin(22, Pin.PULL_UP), sda=Pin(23, Pin.PULL_UP)) # create I2C bus

############## 3.3.1 Initialize Accelerometer ################
# check Device ID
# configure the following settings in the ADXL3343 using I2C #
##############################################################
# get accelerometer addr
addr_read = i2c.scan()
acm_addr = addr_read[1] 

# if Device ID incorrect, print error message
devid_read = i2c.readfrom_mem(acm_addr, 0x00, 1)
devid_correct = b'\xe5'
if (devid_correct != devid_read):
    print('Device ID is inaccessible or incorrect. Exiting program...')
    sys.exit()

# set to 10-bit full-resoution mode for output
# Register 0x31 - Data_format; set FULL_RES bit (D3) to 0
# set range to +/-2g
# Register 0x31 - Data_format; set range bits (D1 & D0) to 00  
i2c.writeto_mem(acm_addr, 0x31, b'\x00') 

# set output data rate (ODR) to 400 Hz 
# Register 0x2C - BW_RATE; set range to 1100
i2c.writeto_mem(acm_addr, 0x2C, b'\x0c')

# this was discussed on Piazza to enable measure mode
# Register 0x2D - Power_CTL; set Measure bit (D3) to 1
i2c.writeto_mem(acm_addr, 0x2D, b'\x08')

############## 3.3.2 Calibrate Accelerometer ##############
# calibrate for when device is flat and still             #                                                         
###########################################################
# x and y should be 0g, z should be 1g to account for gravity
# I calculated that z should be set to 64 base 10 (double check)
i2c.writeto_mem(acm_addr, 0x1E, b'0x00') # x
i2c.writeto_mem(acm_addr, 0x1F, b'0x00') # y
i2c.writeto_mem(acm_addr, 0x20, b'0x40') # z

print("Accelerometer has been calibrated.")

############## 4 IFTTT and ThingSpeak ##############
# 
####################################################

# connect to internet and print local IP (From Lab 3)
connect('Andie', 'alevens1')

# check if Motion Sensor is activated or not by reading data from ThingSpeak
# Hardware Timer every 30 seconds
API_KEY_READ = "FJVB6CAQ1GB79AKH"
timer_thingspeak.init(period=30000, mode=Timer.PERIODIC, callback= lambda t: thingspeak_timer(1))


