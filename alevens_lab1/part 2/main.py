from machine import Pin
from time import sleep

# Onboard RED LED is connected to IO_21
# Create output pin on GPIO_21
led_board = Pin(21, Pin.OUT)

# Toggle LED 5 times
for i in range(10):
    # Change pin value from its current value, value can be 1/0
    led_board.value(not led_board.value())
    sleep(0.5)   # 0.5 seconds delay
    
print("Led blinked 5 times")

