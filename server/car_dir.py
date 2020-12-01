#! /usr/bin/python
# File name   : car_dir.py
# Description : By controlling Servo,thecamera can move Up and down,left and right and the Ultrasonic wave can move to left and right.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/08/22
from __future__ import division
import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

def num_import_int(initial):       #Call this function to import data from '.txt' file
    with open("set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

dir_mid = num_import_int('E_C1:')
dis_mid = num_import_int('E_C2:')

print('dir_mid=%d\n'%dir_mid)
print('dis_mid=%d\n'%dis_mid)

add=dir_mid
cat=dir_mid
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def dir_home(dir_ch):
    pwm.set_pwm(dir_ch, 0, dir_mid)

def dir_left(dir_ch):#Camera moves left
    global add
    if add >= 565:
        print("teering gear reached its peak")
    else:
        add+=10
    pwm.set_pwm(dir_ch, 0, add)
def dir_right(dir_ch):#Camera moves right
    global add
    if add <= 265:
        print("teering gear reached its peak")
    else:
        add-=10
        pwm.set_pwm(dir_ch, 0, add)

def dis_home(dis_ch):#Ultrasound initial position
    pwm.set_pwm(dis_ch, 0, dis_mid)

def dis_left(dis_ch):#Ultrasound moves left
    pwm.set_pwm(dis_ch, 0, dis_mid+240)

def dis_right(dis_ch):#Ultrasound moves right
    pwm.set_pwm(dis_ch, 0, dis_mid-160)

def dir_Left(dir_ch):#Camera moves up
    global cat
    if cat >= 580:
        print("teering gear reached its peak")
    else:
        cat+=10
    pwm.set_pwm(dir_ch, 0, cat)

def dir_Right(dir_ch):#Camera moves down
    global cat
    if cat <= 270:
        print("teering gear reached its peak")
    else:
        cat-=10
        pwm.set_pwm(dir_ch, 0, cat)

def dir_Right_scan(dir_ch,cat):#Camera moves down
    if cat <= 270:
        return False
    else:
        cat-=1
        pwm.set_pwm(dir_ch, 0, cat)