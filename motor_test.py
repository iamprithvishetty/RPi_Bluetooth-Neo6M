import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Motor1_0 = 19
Motor1_1 = 26

Motor2_0 = 20
Motor2_1 = 21

GPIO.setup(Motor1_0,GPIO.OUT)
GPIO.setup(Motor1_1,GPIO.OUT)
GPIO.setup(Motor2_0,GPIO.OUT)
GPIO.setup(Motor2_1,GPIO.OUT)

GPIO.output(Motor1_0,True)
GPIO.output(Motor1_1,False)
            
GPIO.output(Motor2_0,True)
GPIO.output(Motor2_1,False)