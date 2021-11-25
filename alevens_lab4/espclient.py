import time, network, ntptime, esp32, machine, socket
from machine import Pin, RTC, TouchPad, Timer, wake_reason

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
   
# 5.2 HTTP GET request as described in the micropython documentation
def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    #while True:
    #    data = s.recv(100)
    #    if data:
    #        print(str(data, 'utf8'), end='')
    #    else:
    #        break
    s.close()
    
def data_timer(i):
    hall = str(esp32.hall_sensor())
    temperature = str(esp32.raw_temperature())
    # display data
    print("Hall: " + hall + "   Temperature: " + temperature)
    # send data to ThingSpeak 
    http_get("https://api.thingspeak.com/update?api_key="+API_KEY+"&field1="+temperature+"&field2="+hall)
 
# Connect to Internet    
connect('Andie', 'alevens1')
API_KEY = "MRCXZL0H8F85D4D7"

# Initialize a hardware timer with a period of 16 seconds
# measures onboard temp and hall data
# displays both data on terminal
# Sends data to Thinkspeak using socket API and HTTP GET Request
timer_data = Timer(0)
timer_data.init(period=16000, mode=Timer.PERIODIC, callback= lambda t: data_timer(1))



