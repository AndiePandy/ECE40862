import time, network, ntptime, esp32, machine, socket, sys, urequests
from machine import Pin, RTC, TouchPad, Timer, wake_reason, I2C       
from struct import unpack
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
    
def status_timer(API_KEY_READ):
    # read data from Thingspeak
    req = urequests.get("https://api.thingspeak.com/channels/1583988/fields/1/last?key="+API_KEY_READ)
    global status
    if (req.text == "activate"):
        status = "activate"
        led_green.value(1)
    elif (req.text == "deactivate"):
        status = "deactivate"
        led_green.value(0)
    req.close()

def notify_timer(acm_addr):
    # send notifications to IFTTT
    
    val1= i2c.readfrom_mem(acm_addr, 0x33, 1) + i2c.readfrom_mem(acm_addr, 0x32, 1)
    val1 = unpack( '>h', val1 )[0]
    val2= i2c.readfrom_mem(acm_addr, 0x35, 1) + i2c.readfrom_mem(acm_addr, 0x34, 1)
    val2 = unpack( '>h', val2 )[0]
    val3= i2c.readfrom_mem(acm_addr, 0x37, 1) + i2c.readfrom_mem(acm_addr, 0x36, 1)
    val3 = unpack( '>h', val3 )[0]


    val1 = (val1/256)
    val2 = (val2/256)
    val3 = (val3/256)
    
    
    if (status=="activate" and (val1 > 0.8 or val2 > 0.8 or val3 > 1.8)):
        led_red.value(1)
        url = "https://maker.ifttt.com/trigger/Motion_Detected/with/key/lxy3OOOO7S4awuW_M69tXwShf837rVsTbrqLbZDBSlL?value1="+str(val1)+"&value2="+str(val2)+"&value3="+str(val3)
        req = urequests.post(url)
        req.close()
    else:
        led_red.value(0)


############## 3.2 Software Init ###################
# Init LEDS, Timers, Interrupts (if needed)        #
# use I2C driver to communicate with Accelerometer #
####################################################
led_red = Pin(21, Pin.OUT)   # Onboard RED LED is connected to IO_21
led_green = Pin(27, Pin.OUT) # Onboard GREEN LED is connected to IO_27
led_red.value(0)             # should be off when init
led_green.value(0)           # should be off when init

timer_status = Timer(0) # init hardware timer to check if activated
timer_notify = Timer(1) # init harware timer for ifttt notifications 

i2c = I2C(1, scl=Pin(22, Pin.PULL_UP), sda=Pin(23, Pin.PULL_UP)) # create I2C bus

status = "deactivate"
############## 3.3.1 Initialize Accelerometer ################
# check Device ID                                            #
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
#       calibrate for when device is flat and still       #                                                         
###########################################################
# x and y should be 0g, z should be 1g to account for gravity
# I calculated that z should be set to 64 base 10
val1= i2c.readfrom_mem(acm_addr, 0x33, 1) + i2c.readfrom_mem(acm_addr, 0x32, 1)
val1 = unpack( '>h', val1 )[0]
val2= i2c.readfrom_mem(acm_addr, 0x35, 1) + i2c.readfrom_mem(acm_addr, 0x34, 1)
val2 = unpack( '>h', val2 )[0]
val3= i2c.readfrom_mem(acm_addr, 0x37, 1) + i2c.readfrom_mem(acm_addr, 0x36, 1)
val3 = unpack( '>h', val3 )[0]

val1 = hex(int(val1/256))
val2 = hex(int(val2/256))
val3 = hex(int(val3/256))

i2c.writeto_mem(acm_addr, 0x1E, val1) # x
i2c.writeto_mem(acm_addr, 0x1F, val2) # y
i2c.writeto_mem(acm_addr, 0x20, val3) # z

print("Accelerometer has been calibrated.")

############## 4 IFTTT and ThingSpeak ##############
#        get notifications and status setup        #
####################################################
API_KEY_READ = "FJVB6CAQ1GB79AKH"
API_KEY_WRITE = "OJMQEMI54VYJ9VJX" # in IFTTT applet 1

# connect to internet and print local IP (From Lab 3)
connect('Andie', 'alevens1')

# check if Motion Sensor is activated or not by reading data from ThingSpeak
# Hardware Timer every 30 seconds
timer_status.init(period=30000, mode=Timer.PERIODIC, callback= lambda t: status_timer(API_KEY_READ))

# send notifications of accelerometer data every 10 seconds IF status == activated
timer_notify.init(period=10000, mode=Timer.PERIODIC, callback= lambda t: notify_timer(acm_addr))



