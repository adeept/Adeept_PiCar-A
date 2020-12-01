#!/usr/bin/env/python3
# Product     : PiCar-A
# File name   : server.py
# Description : The main program server takes control of Ultrasonic,Motor,Servo by receiving the order from the client through TCP and carrying out the corresponding operation.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/12/18

import RPi.GPIO as GPIO
from multiprocessing import Process
import os
import motor
import car_dir 
import ultrasonic
import auto
import socket
import FPV
import time
import threading
from  threading import *
import Adafruit_PCA9685
import picamera

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)
pwm = Adafruit_PCA9685.PCA9685()    #Ultrasonic Control

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    newline=""
    str_num=str(new_num)
    with open(thisPath + "/set.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num+"\n")
            newline += line
    with open(thisPath + "/set.txt","w") as f:
        f.writelines(newline)

def num_import_int(initial):        #Call this function to import data from '.txt' file
    with open(thisPath + "/set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

spd_ad     = 1          #Speed Adjustment
pwm0       = 0          #Camera direction 
pwm1       = 1          #Ultrasonic direction
b_spd      = num_import_int('E_M1:')         #Speed of the car
t_spd      = num_import_int('E_M2:')         #Speed of the car
left       = num_import_int('E_T1:')         #Motor Left
right      = num_import_int('E_T2:')         #Motor Right
dir_mid    = num_import_int('E_C1:')
dis_mid    = num_import_int('E_C2:')

print('b_spd=%d\n'%b_spd)
print('t_spd=%d\n'%t_spd)
print('left=%d\n'%left)
print('right=%d\n'%right)

status     = 1          #Motor rotation
forward    = 0          #Motor forward
backward   = 1          #Motor backward
dis_dir    = []         #Result of Ultrasonic Scanning
ip_con     = ''

def scan():             #Ultrasonic Scanning
    global dis_dir
    car_dir.dis_home(pwm1)   #Ultrasonic point forward
    car_dir.dis_left(pwm1)   #Ultrasonic point Left,prepare to scan
    dis_dir=['list']         #Make a mark so that the client would know it is a list
    time.sleep(0.5)          #Wait for the Ultrasonic to be in position
    cat_2=600                #Value of left-position
    GPIO.setwarnings(False)  #Or it may print warnings
    while cat_2>190:         #Scan,from left to right
        pwm.set_pwm(pwm1, 0, cat_2)
        cat_2 -= 1           #This value determine the speed of scanning,the greater the faster
        new_scan_data=round(ultrasonic.checkdist(),2)   #Get a distance of a certern direction
        dis_dir.append(str(new_scan_data))              #Put that distance value into a list,and save it as String-Type for future transmission 
    car_dir.dis_home(pwm1)   #Ultrasonic point forward
    return dis_dir

def setup():                #initialization
    motor.setup()           #Motor initialization
    car_dir.dir_home(pwm0)  #Initial position of the camera
    car_dir.dir_home(pwm1)  #Initial position of the ultrasonic

def autoMode():             #Autopilot
    auto.loop()

class Job(threading.Thread):#Threads for Auto Mode
    def __init__(self,*args,**kwargs):
        super(Job,self).__init__(*args,**kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
    
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            autoMode()
            time.sleep(1)
    
    def pause(self):
        self.__flag.clear()
    
    def resume(self):
        self.__flag.set()
    
    def stop(self):
        self.__flag.set()
        self.__running.clear()


def FPV_thread():
    fpv=FPV.FPV()
    print(addr[0])
    fpv.capture_thread(addr[0])


def run():            #Main function
    global ip_con, addr
    st_s = 0
    while True:
        #print('SET %s'%dir_mid+' %s'%dis_mid+' %s'%b_spd+' %s'%t_spd+' %s'%left+' %s'%right)
        print('waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()#Determine whether to connect
        print('...connected from :', addr)
        tcpCliSock.send(('SET %s'%dir_mid+' %s'%dis_mid+' %s'%b_spd+' %s'%t_spd+' %s'%left+' %s'%right).encode())
        break

    fps_threading=threading.Thread(target=FPV_thread)         #Define a thread for FPV and OpenCV
    fps_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    fps_threading.start()                                     #Thread starts
    st = Job()
    while True: 
        data = ''
        data = tcpCliSock.recv(BUFSIZ).decode()#Get instructions
        #print(data)
        if not data:
            continue
        
        elif 'spdset' in data:
            global spd_ad
            try:
                spd_ad=float((str(data))[7:])      #Speed Adjustment
            except:
                print('wrong speed value')
        
        elif 'EC1set' in data:                 #Camera Adjustment
            try:
                new_EC1=int((str(data))[7:])
                replace_num('E_C1:',new_EC1)
            except:
                pass

        elif 'EC2set' in data:                 #Ultrasonic Adjustment
            try:
                new_EC2=int((str(data))[7:])
                replace_num('E_C2:',new_EC2)
            except:
                pass

        elif 'EM1set' in data:                 #Motor A Speed Adjustment
            try:
                new_EM1=int((str(data))[7:])
                replace_num('E_M1:',new_EM1)
            except:
                pass

        elif 'EM2set' in data:                 #Motor B Speed Adjustment
            try:
                new_EM2=int((str(data))[7:])
                replace_num('E_M2:',new_EM2)
            except:
                pass

        elif 'ET1set' in data:                 #Motor A Turningf Speed Adjustment
            try:
                new_ET1=int((str(data))[7:])
                replace_num('E_T1:',new_ET1)
            except:
                pass

        elif 'ET2set' in data:                 #Motor B Turningf Speed Adjustment
            try:
                new_ET2=int((str(data))[7:])
                replace_num('E_T2:',new_ET2)
            except:
                pass

        elif 'scan' in data:
            dis_can=scan()                     #Start Scanning
            str_list_1=dis_can                 #Divide the list to make it samller to send 
            str_index=' '                      #Separate the values by space
            str_send_1=str_index.join(str_list_1)+' '
            tcpCliSock.sendall((str(str_send_1)).encode())   #Send Data
            tcpCliSock.send('finished'.encode())        #Sending 'finished' tell the client to stop receiving the list of dis_can
        
        elif 'forward' in data:                #When server receive "forward" from client,car moves forward
            tcpCliSock.send('1'.encode())
            motor.motor(status, forward, b_spd*spd_ad)
            motor.motor1(status,forward,t_spd*spd_ad)
            direction = forward
        
        elif 'backward' in data:               #When server receive "backward" from client,car moves backward
            tcpCliSock.send('2'.encode())
            motor.motor(status, backward, b_spd*spd_ad)
            motor.motor1(status, backward, t_spd*spd_ad)
            direction = backward
        
        elif 'left' in data:                   #When server receive "left" from client,camera turns left
            tcpCliSock.send('7'.encode())
            car_dir.dir_left(pwm1)
            #car_dir.dir_right(pwm1)
            continue
        
        elif 'right' in data:                  #When server receive "right" from client,camera turns right
            tcpCliSock.send('8'.encode())
            car_dir.dir_right(pwm1)
            #car_dir.dir_left(pwm1)
            continue
        
        elif 'on' in data:                     #When server receive "on" from client,camera looks up
            tcpCliSock.send('5'.encode())
            car_dir.dir_Left(pwm0)
            #car_dir.dir_Right(pwm0)
            continue
        
        elif 'under' in data:                  #When server receive "under" from client,camera looks down
            tcpCliSock.send('6'.encode())
            car_dir.dir_Right(pwm0)
            #car_dir.dir_Left(pwm0)
            continue
        
        elif 'Left' in data:                   #When server receive "Left" from client,car turns left
            tcpCliSock.send('3'.encode())
            motor.motor(status, forward, left*spd_ad)
            motor.motor1(status, forward, b_spd*spd_ad)
            #print('LLL')
            continue

        elif 'BLe' in data:                    #When server receive "BLeft" from client,car move back and left
            tcpCliSock.send('3'.encode())
            motor.motor(status, backward, left*spd_ad)
            motor.motor1(status, backward, b_spd*spd_ad)
            #print("BL")
            continue

        elif 'Right' in data:                  #When server receive "Right" from client,car turns right
            tcpCliSock.send('4'.encode())
            motor.motor(status, forward, b_spd*spd_ad)
            motor.motor1(status, forward, right*spd_ad)
            continue

        elif 'BRi' in data:                    #When server receive "BRight" from client,car move back and right
            tcpCliSock.send('4'.encode())
            motor.motor(status, backward, b_spd*spd_ad)
            motor.motor1(status, backward, right*spd_ad)
            continue
        
        elif 'exit' in data:                   #When server receive "exit" from client,server shuts down
            GPIO.cleanup()
            tcpSerSock.close()
            os.system('sudo init 0')
            continue
        
        elif 'stop' in data:                   #When server receive "stop" from client,car stops moving
            tcpCliSock.send('9'.encode())
            #setup()
            motor.motorStop()
            #GPIO.cleanup()
            #setup()
            continue
        
        elif 'home' in data:                   #When server receive "home" from client,camera looks forward
            car_dir.dir_home(pwm0)
            car_dir.dir_home(pwm1)
            continue
        
        elif 'Stop' in data:                   #When server receive "Stop" from client,Auto Mode switches off
            tcpCliSock.send('9'.encode())
            try:
                st.pause()
            except:
                pass
            motor.motorStop()
            time.sleep(0.4)
            motor.motorStop()
        
        elif 'auto' in data:                   #When server receive "auto" from client,start Auto Mode
            tcpCliSock.send('0'.encode())
            if st_s == 0:
                st.start()
                st_s = 1
            else:
                st.resume()
            continue


        else:
            pass

def destroy():
    GPIO.cleanup()
    connection.close()
    client_socket.close()

if __name__ == '__main__':

    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)                      #Start server,waiting for client

    setup()
    try:
        run()
    except KeyboardInterrupt:
        destroy()
        tcpClicSock.close()          # Close socket or it may not connect with the server again
        cv2.destroyAllWindows()

