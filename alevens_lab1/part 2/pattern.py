from machine import Pin
from time import sleep

# Onboard RED LED is connected to IO_21
led_red = Pin(21, Pin.OUT)

# Onboard GREEN LED is connected to IO_13
led_green = Pin(13, Pin.OUT)

# RED push button is connected to IO_15
push_red = Pin(15, Pin.IN)

# GREEN push button is connected IO_14
push_green = Pin(14, Pin.IN)

# counters
count_green = 0
count_red = 0
a = 1
i = 1
#put while true and program breaks once a switch has been pressed 10 times total and the other switch was pressed afterward
while(a == 1):
    # if input on green and no input on red, turn green on, leave red off, increment green count
    if(push_green.value() == 1 and push_red.value() == 0):
        #print("green on")
        led_green.value(1)
        led_red.value(0)
        if(push_green.value() == 0):
            print("green count")
            count_green += 1

    # if input on red and no input on green, turn red on, leave green off, increment red count
    if(push_red.value() == 1 and push_green.value() == 0):
        #print("red on")
        led_red.value(1)
        led_green.value(0)
        if(push_red.value() == 0):
            print("red count")
            count_red += 1

    # if both on, turn both leds off, increment both counts
    if(push_red.value() == 1 and push_green.value() == 1):
        led_red.value(0)
        led_green.value(0)
        if(push_green.value() == 0 and push_red.value() == 0):
            count_red += 1
            count_green += 1

    # if both off, turn both leds off, leave counters alone
    if(push_red.value() == 0 and push_green.value() == 0):
        led_red.value(0)
        led_green.value(0)

    # counter for each led should count until ten
    # if count_red or count_green = 10, blink alternatively (two different if statements)(maybe 3 if both = 10)
    # to blink alternatively, use for loop like in previous program and break(twice) if different switch pushed
    # once other switch pressed, break and print success message
    if(count_red == 10 or (count_red == 10 and count_green == 10)):
        print("red == 10")
        led_red.value(1)
        led_green.value(0)
        while(i == 1):
            led_red.value(not led_red.value())
            led_green.value(not led_green.value())
            sleep(0.5)   # 0.5 seconds delay
            if(push_green.value() == 1):
                led_green.value(0)
                led_red.value(0)
                a = 0
                i=0
                print("You have successfully implemented LAB1 DEMO!!!a")
        
    if(count_green == 10):
        print("green == 10")
        led_red.value(0)
        led_green.value(1)
        while(i == 1):
            led_red.value(not led_red.value())
            led_green.value(not led_green.value())
            sleep(0.5)   # 0.5 seconds delay
            if(push_green.value() == 1):
                led_green.value(0)
                led_red.value(0)
                a = 0
                i=0
                print("You have successfully implemented LAB1 DEMO!!!b")
        
    

    

    




