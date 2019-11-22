from Config import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IO_PORT,GPIO.OUT)
GPIO.cleanup()

