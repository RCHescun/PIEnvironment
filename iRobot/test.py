from Config import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IO_PORT,GPIO.OUT)

#GPIO.cleanup()
import time
while True:
    GPIO.cleanup()
    time.sleep(1) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IO_PORT,GPIO.OUT)   
    GPIO.output(IO_PORT,GPIO.LOW)
    time.sleep(1)
