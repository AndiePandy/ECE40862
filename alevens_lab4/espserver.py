import time, network, ntptime, esp32, machine, socket
from machine import Pin, RTC, TouchPad, Timer, wake_reason

# Global variables
temp = esp32.raw_temperature()# measure temperature sensor data
hall = esp32.hall_sensor() # measure hall sensor data
red_led_state = "ON" # string, check state of red led, ON or OFF
green_led_state = "ON" # string, check state of red led, ON or OFF
switch_state = "Not Pressed"


def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state, green_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Switch</span>
    <span>"""+switch_state+"""</span>
    <sup class="units"></sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage

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

# Connect to Internet and print local IP (from lab 3)
connect('Andie', 'alevens1')

# set up pins
led_red = Pin(21, Pin.OUT) # Onboard RED LED is connected to IO_21
led_green = Pin(27, Pin.OUT) # Onboard GREEN LED is connected to IO_27
push = Pin(15, Pin.IN, Pin.PULL_DOWN) # Push Button is connected to IO_15

# Create HTTP server using socket API
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)

# Use infinite loop
while(True):
    # connect
    conn, addr = s.accept()
    print(addr)
    request = str(conn.recv(1024))
    #print('Content = %s' % request)
    
    # Measure temp and hall
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    if push.value() == 1:
        switch_state = "Pressed"
    else:
        switch_state = "Not pressed"
    # Measure LED values
    # red led
    red_on = request.find('/?red_led=on')
    red_off = request.find('/?red_led=off')
    if red_on == 6:
        led_red.value(1)
        red_led_state = "ON"
    if red_off == 6:
        led_red.value(0)
        red_led_state = "OFF"
        
    # green led
    green_on = request.find('/?green_led=on')
    green_off = request.find('/?green_led=off')
    if green_on == 6:
        led_green.value(1)
        green_led_state = "ON"
    if green_off == 6:
        led_green.value(0)
        green_led_state = "OFF"


    # Use web_page function to create HTML text to build webpage
    # with sensor data and LED values
    page = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(page)
    conn.close()
    
    





