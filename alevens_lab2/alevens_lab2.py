from machine import Pin, ADC, PWM, RTC, Timer

# Defined Functions
def print_datetime(datetime):
    # display current date and time
    print("Date: ", datetime[0],datetime[2],datetime[1],datetime[3])
    print("Time: ", datetime[4], datetime[5], datetime[6], datetime[7])

count_press = 0
def pushPress(pin):
    # increment the current number of times the push button has been pressed
    global count_press
    count_press = count_press + 1
    
# User Inputs
year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? ")) # 0-6 for Monday-Sunday
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
microsecond = int(input("Microsecond? "))

# use User Inputs with RTC
rtc = RTC()
rtc.datetime((year,month,day,weekday,hour,minute,second,microsecond))

# display the current date and time every 30 seconds
timer_30s = Timer(0)
timer_30s.init(period=30000, mode=Timer.PERIODIC, callback= lambda t: print_datetime(rtc.datetime()))

# read the analog input (pot values) every 100ms
# potentiometer connected to pin A2 (pin 34) - ADC #1
adc = ADC(Pin(34))
timer_adc = Timer(1)
timer_adc.init(period=100, mode=Timer.PERIODIC, callback=lambda t:adc.read())

# start a PWM signal on the external LED using a frequency of 10 Hz and a duty cycle of 256
# When count_press == 0, pot should do nothing
pwm_red = PWM(Pin(21), freq=10, duty=256)

# Detect a switch press using an interrupt/callback
# I decided to interrupt on rising edge
# pushbutton connected to IO_15
push = Pin(15, Pin.IN, Pin.PULL_DOWN)
push.irq(handler = pushPress, trigger=Pin.IRQ_RISING)

while True:
    # When count_press is even, control duty cycle
    if (count_press % 2 != 0) and (count_press > 0):
        pwm_red.freq(adc.read())
    # When odd, control freq
    elif (count_press %2 == 0) and (count_press > 0):
        pwm_red.duty(adc.read())