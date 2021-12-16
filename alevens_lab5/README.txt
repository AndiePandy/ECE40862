ECE 40862 Lab 5
Andrea Renee Levenson (alevens)

Video Submission Link - Video should be unlisted. Please let me know if it is not. 

https://youtu.be/iyzPH4eCasY



Pins
RED LED       Pin 21
GREEN LED     Pin 27
SCL           Pin 22
SDA           Pin 23



Brief Description
I'm just going to list how I did things in chronological order, not in order of the document necessarily

First, I initialized all the leds I could and created the i2c bus using the scl and sda pins. After, I made sure the program checked
that the device id read is xe5 as documented in the ADXL343 datasheet. I also made sure the data format register (0x31), the BW_RATE 
register (0x2C), and POWER_CTL register (0x2d) were configured according to the lab5 document. The exact bits I calibrated are 
commented in the code. I then calibrated the offset registers (0x1E, 0x1F, 0x20) according the the current data readings. Next, I set 
up Thingspeak and IFTTT according the the lab document. I had a timer check the status of the Sensor_state every 30 seconds to check if 
the motion sensor had been activated or deactivated. Every 10 seconds, the accelerometers motion is checked and if it is moving, the red 
led turns on and a notification of the data is sent to the phone.