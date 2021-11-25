from machine import Pin, RTC, TouchPad, Timer, wake_reason
import time, network, ntptime, esp32, machine

# Onboard RED LED is connected to IO_21
led_red = Pin(21, Pin.OUT)
led_red.value(1) # on when the ESP32 is awake

# Defined Functions

# inspired by micropython documentation for network module
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
    

def print_datetime(datetime):
    # display current date and time
    print("Date: "+str(datetime[1])+'/'+str(datetime[2])+'/'+str(datetime[0]))
    print("Time: "+str(datetime[4])+':'+str(datetime[5])+':'+str(datetime[6])+' HRS\n')

def read_touch(wire_touch, led_green):
    # check if wire is being touched
    # small values -> touch present; large values -> no touch present
    # touch present -> led on, otherwise off
    if wire_touch.read() <= 300:
        led_green.value(1)
    else:
        led_green.value(0)

def deepSleep_timer(push):
    esp32.wake_on_ext0(pin = push, level = esp32.WAKEUP_ANY_HIGH)
    print('I am going to sleep for 1 minute.\n')
    machine.deepsleep(60000)

if (wake_reason() == 2):
    print("\nEXT0 Wake Up\n")
elif (wake_reason() == 4):
    print("\nTimer Wake Up\n")

# 2.2.1. connect to the internet over WiFi
connect('Andie', 'alevens1')

# 2.2.2. display current date/time using ntptime
rtc = RTC()
ntptime.settime()
y, m, d, wd, hr, minute, sec, msec = rtc.datetime()
rtc.datetime((y, m, d, wd, hr-4, minute, sec, msec))
# display every 15 seconds with hardware timer
timer_date = Timer(0)
timer_date.init(period=15000, mode=Timer.PERIODIC, callback= lambda t: print_datetime(rtc.datetime()))

# 2.2.3. Green LED Control by Touch Input
# Onboard GREEN LED is connected to IO_27
led_green = Pin(27, Pin.OUT) 
wire_touch = TouchPad(Pin(12))

timer_touch = Timer(1)
timer_touch.init(period=50, mode=Timer.PERIODIC, callback= lambda t: read_touch(wire_touch, led_green))

# 2.2.4. Red LED, Deep Sleep and Different Wake Up Sources
# put ESP32 in deep sleep every 30 seconds for 1 min with timer
push = Pin(15, Pin.IN, Pin.PULL_DOWN)
timer_deepSleep = Timer(2)
timer_deepSleep.init(period=30000, mode=Timer.PERIODIC, callback= lambda t: deepSleep_timer(push))


    


