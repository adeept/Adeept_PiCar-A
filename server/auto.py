#!/usr/bin/evn python
# File name   : auto.py
# Description : By detecting the distance through Ultrasonic,controlling the RPi car move to the four directons:the front,back,left and right,thus the car achieves automatic avoidance.  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/08/22
import RPi.GPIO as GPIO
import motor
import ultrasonic
import car_dir
import time
import os

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)
def num_import_int(initial):       #Call this function to import data from '.txt' file
    with open(thisPath + "/set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

b_spd      = num_import_int('E_M1:')         #Speed of the car
t_spd      = num_import_int('E_M2:')         #Speed of the car
left       = num_import_int('E_T1:')         #Motor Left
right      = num_import_int('E_T2:')         #Motor Right
pwm0     = 0
pwm1     = 1
dis      = 0.7 #the stop distance
mindis   = 0.65#Change the distance of the car's behavior
status   = 1    
forward  = 0
backward = 1

def setup():#initialization
    motor.setup()
        
def loop():
    car_dir.dis_home(pwm1)#Ultrasound initial position
    time.sleep(0.5)
    a = ultrasonic.checkdist()#Get the ultrasonic detection distance
    b = ultrasonic.checkdist()#Get the ultrasonic detection distance
    c = ultrasonic.checkdist()#Get the ultrasonic detection distance
    homedis = min(a,b,c)#Get the ultrasonic detection distance
    
    print('homedis = %0.2f m' %homedis)
    
    motor.motorStop()#Stop the car
    
    if homedis > dis:#No obstacles
        motor.motor(status, forward, b_spd)
        motor.motor1(status, forward, t_spd)
    elif homedis < dis:#Obstacles
        car_dir.dis_left(pwm1)
        time.sleep(1)
        a = ultrasonic.checkdist()
        b = ultrasonic.checkdist()
        c = ultrasonic.checkdist()
        leftdis = min(a,b,c)
        print('leftdis = %0.2f m' %leftdis)
        car_dir.dis_right(pwm1)
        time.sleep(1)
        a = ultrasonic.checkdist()
        b = ultrasonic.checkdist()
        c = ultrasonic.checkdist()
        rightdis = min(a,b,c)
        print('rightdis = %0.2f m' %rightdis)
        
        if leftdis < dis and  rightdis < dis:#Judgment left and right
            if leftdis >= rightdis:#There are obstacles on the right
                motor.motor(status, backward, b_spd)
                #motor.motor(status,backward,left)
                #motor.motor1(status,backward,t_spd)
                motor.motor1(status,backward,right)
                time.sleep(1)
                motor.motor(status,forward,left)
                motor.motor1(status,forward,b_spd)
                time.sleep(0.5)
            else:#There are obstacles on the left
                motor.motor(status,backward,left)
                motor.motor1(status,backward,t_spd)
                time.sleep(1)
                motor.motor(status,forward,b_spd)
                motor.motor1(status,forward,right)
                time.sleep(0.5)
        elif leftdis > dis and rightdis <= dis:#There are obstacles on the right
            if homedis < mindis:#Obstacle ahead
                motor.motor(status, backward, b_spd)
                motor.motor1(status, backward, t_spd)
                time.sleep(1)
                motor.motor(status, forward, left)
                motor.motor1(status, forward, b_spd)
                time.sleep(0.5)
            else:#No obstacle ahead
                motor.motor(status, forward, left)
                motor.motor1(status, forward, b_spd)
                time.sleep(0.5)
        elif rightdis > dis and leftdis <= dis:#There are obstacles on the left
            if homedis < mindis:#Obstacle ahead
                motor.motor(status, backward, b_spd)
                motor.motor1(status, backward, t_spd)
                time.sleep(1)
                motor.motor(status, forward, b_spd)
                motor.motor1(status, forward, right)
                time.sleep(0.5)
            else:#No obstacle ahead
                motor.motor(status, forward, b_spd)
                motor.motor1(status, forward, right)
                time.sleep(0.5)
        elif rightdis > dis and leftdis > dis:#There are no obstacles
            if rightdis > leftdis:#The distance to the right is greater than the left
                if homedis < mindis:#Obstacle ahead
                    motor.motor(status, backward, b_spd)
                    motor.motor1(status, backward, t_spd)
                    time.sleep(1)
                motor.motor(status, forward, b_spd)
                motor.motor1(status, forward, right)
                time.sleep(0.5)
            else:#No obstacle ahead
                motor.motor(status, forward, b_spd)
                motor.motor1(status, forward, right)
                time.sleep(0.5)
        elif rightdis < leftdis:#The distance to the left is greater than the right
            if homedis < mindis:#Obstacle ahead
                motor.motor(status, backward, b_spd)
                motor.motor1(status, backward, t_spd)
                time.sleep(1)
                motor.motor(status, forward, left)
                motor.motor1(status, forward, b_spd)
                time.sleep(0.5)
            else:#NO Obstacle ahead
                motor.motor(status, forward, left)
                motor.motor1(status, forward, b_spd)
                time.sleep(0.5)
        elif leftdis == rightdis:
            motor.motor(status, backward, b_spd)
            motor.motor1(status, backward, t_spd)
            time.sleep(1) 
def destroy():
    motor.destroy()
    GPIO.cleanup()


try:
    pass
except KeyboardInterrupt:
    destroy()
