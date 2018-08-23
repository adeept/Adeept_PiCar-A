#! /usr/bin/python
# File name   : Ultrasonic.py
# Description : Detection distance  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : Code
# Date        : 2018/08/22
import RPi.GPIO as GPIO
import time

Tr = 23
Ec = 24

def checkdist():#Reading distance
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(Ec, GPIO.IN)
	GPIO.output(Tr, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(Tr, GPIO.LOW)
	while not GPIO.input(Ec):
		pass
	t1 = time.time()
	while GPIO.input(Ec):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

try:
        pass

except KeyboardInterrupt:
	GPIO.cleanup()
