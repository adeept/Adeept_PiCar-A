#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/08/22
from socket import *
import sys,subprocess
import time
import threading as thread
import tkinter as tk
import math

stat=0          #A status value,ensure the mainloop() runs only once
tcpClicSock=''  #A global variable,for future socket connection
BUFSIZ=1024     #Set a buffer size
ip_stu=1        #Shows connection status

#Global variables of input status
c_f_stu=0
c_b_stu=0
c_l_stu=0
c_r_stu=0

b_l_stu=0
b_r_stu=0

l_stu=0
r_stu=0

BtnIP=''
ipaddr=''
ipcon=0

def replace_path(initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open("VLC.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num)
            newline += line
    with open("VLC.txt","w") as f:
        f.writelines(newline)  #Call this function to replace data in '.txt' file

def import_path(initial):
    with open("VLC.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=snum
    return n             #Call this function to import data from '.txt' file

def video_show():
    global ipcon
    server_socket = socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    connection = server_socket.accept()[0].makefile('rb')
    try:
        vlc_path=import_path('addr:')
        cmdline = [vlc_path, '--demux', 'h264', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        while True:
            try:
                data = connection.read(128)
                if not data:
                    break
            except:
                pass
            try:
                player.stdin.write(data)
            except:
                connection.close()
                server_socket.close()
                player.terminate()                     #Call this function to set up a server for the car to send the video back
                BtnIP.config(state='normal')
                ipcon=0
                break
    finally:
        connection.close()
        server_socket.close()
        player.terminate()                     #Call this function to set up a server for the car to send the video back
        BtnIP.config(state='normal')
        ipcon=0

def ip_send():
    time.sleep(1)
    tcpClicSock.send(('IPCON %s'%ipaddr).encode())
    print(ipaddr)                        #Call this function to send the IP of server to client(only for video stream)

def call_forward(event):         #When this function is called,client commands the car to move forward
    global c_f_stu
    if (c_f_stu == 0) & ((l_stu+r_stu)==0):
        tcpClicSock.send(('forward').encode())
        print('forward')
        c_f_stu=1

def call_back(event):            #When this function is called,client commands the car to move backward
    global c_b_stu 
    if c_l_stu == 1:
        tcpClicSock.send(('BLe').encode())
        print('Backward Left')
        c_b_stu=1
    elif c_r_stu == 1:
        tcpClicSock.send(('BRi').encode())
        print('Backward Right')
        c_b_stu=1
    elif c_b_stu == 0:
        tcpClicSock.send(('backward').encode())
        print('Backward')
        c_b_stu=1

def call_left(event):            #When this function is called,client commands the camera to look left
    tcpClicSock.send(('left').encode())

def call_right(event):           #When this function is called,client commands the camera to look right
    tcpClicSock.send(('right').encode())

def call_Left(event):            #When this function is called,client commands the car to turn left
    global c_l_stu,b_l_stu
    if c_l_stu == 0 & c_b_stu==0:
        tcpClicSock.send(('Left').encode())
        print('Turn Left')
        c_l_stu=1
        if c_b_stu == 1:
            print(c_b_stu)
            tcpClicSock.send(('BLe').encode())
            print('Backward Left')
            b_l_stu=1

def call_Right(event):           #When this function is called,client commands the car to turn right
    global c_r_stu,b_r_stu
    if c_r_stu == 0 & c_b_stu==0:
        tcpClicSock.send(('Right').encode())
        print('Turn Right')
        c_r_stu=1
        if c_b_stu == 1:
            tcpClicSock.send(('BRi').encode())
            print('Backward Right')
            b_r_stu=1

def call_stop(event):            #When this function is called,client commands the car to stop moving
    global c_f_stu,c_b_stu,c_l_stu,c_r_stu
    c_f_stu=0
    c_b_stu=0
    c_l_stu=0
    c_r_stu=0

    b_l_stu=0
    b_r_stu=0

    l_stu=0
    r_stu=0

    tcpClicSock.send(('stop').encode())
    print('Stop')

def call_home(event):            #When this function is called,client commands the camera to look forward
    tcpClicSock.send(('home').encode())

def call_under(event):           #When this function is called,client commands the car to look down
    tcpClicSock.send(('under').encode())

def call_on(event):              #When this function is called,client commands the car to look up
    tcpClicSock.send(('on').encode())

def call_auto(event):            #When this function is called,client commands the car to start auto mode
    tcpClicSock.send(('auto').encode())

def call_exit(event):            #When this function is called,client commands the car to shut down
    tcpClicSock.send(('exit').encode())

def call_Stop(event):            #When this function is called,client commands the car to switch off auto mode
    tcpClicSock.send(('Stop').encode())

def scan(event):                 #When this function is called,client commands the ultrasonic to scan
    tcpClicSock.send(('scan').encode())

def replace_num(initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open("ip.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num)
            newline += line
    with open("ip.txt","w") as f:
        f.writelines(newline)    #Call this function to replace data in '.txt' file

def num_import(initial):
    with open("ip.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=snum
    return n               #Call this function to import data from '.txt' file

def num_import_2(initial):
    with open("VLC.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=snum
    return n             #Call this function to import data from '.txt' file

def loop():                       #GUI
    global tcpClicSock,BtnIP      #The value of tcpClicSock changes in the function loop(),would also changes in global so the other functions could use it.
    while True:
        color_bg='#000000'        #Set background color
        color_text='#E1F5FE'      #Set text color
        color_btn='#212121'       #Set button color
        color_line='#01579B'      #Set line color
        color_can='#212121'       #Set canvas color
        color_oval='#2196F3'      #Set oval color

        root = tk.Tk()            #Define a window named root
        root.title('Adeept')      #Main window title
        root.geometry('917x630')  #Main window size, middle of the English letter x.
        root.config(bg=color_bg)  #Set the background color of root window

        can_scan = tk.Canvas(root,bg=color_can,height=300,width=740,highlightthickness=0) #define a canvas
        can_scan.place(x=30,y=90) #Place the canvas
        
        var_spd = tk.StringVar()  #Speed value saved in a StringVar
        var_spd.set(1)            #Set a default speed,but change it would not change the default speed value in the car,you need to click button'Set' to send the value to the car
        
        var_x_scan = tk.IntVar()  #Scan range value saved in a IntVar
        var_x_scan.set(2)         #Set a default scan value

        logo =tk.PhotoImage(file = 'logo.png')         #Define the picture of logo,but only supports '.png' and '.gif'
        l_logo=tk.Label(root,image = logo,bg=color_bg) #Set a label to show the logo picture
        l_logo.place(x=30,y=13)                        #Place the Label in a right position

        line = can_scan.create_line(0,75,740,75,fill='darkgray') #Draw a line on canvas
        line = can_scan.create_line(0,150,740,150,fill='darkgray') #Draw a line on canvas
        line = can_scan.create_line(0,225,740,225,fill='darkgray') #Draw a line on canvas

        arc_1 = can_scan.create_arc(185,150,555,450,outline='darkgray',extent=180,style='arc')    #Draw a arc on canvas
        arc_1 = can_scan.create_arc(0,0,740,600,outline='darkgray',extent=180,style='arc')    #Draw a arc on canvas

        BtnC1 = tk.Button(root, width=15, text='Camera Middle',fg=color_text,bg=color_btn,relief='ridge')
        BtnC1.place(x=785,y=10)
        E_C1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_C1.place(x=785,y=45)                            #Define a Entry and put it in position

        BtnC2 = tk.Button(root, width=15, text='Ultrasonic Middle',fg=color_text,bg=color_btn,relief='ridge')
        BtnC2.place(x=785,y=100)
        E_C2 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_C2.place(x=785,y=135)                             #Define a Entry and put it in position

        BtnM1 = tk.Button(root, width=15, text='Motor A Speed',fg=color_text,bg=color_btn,relief='ridge')
        BtnM1.place(x=785,y=190)
        E_M1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_M1.place(x=785,y=225)                             #Define a Entry and put it in position

        BtnM2 = tk.Button(root, width=15, text='Motor B Speed',fg=color_text,bg=color_btn,relief='ridge')
        BtnM2.place(x=785,y=280)
        E_M2 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_M2.place(x=785,y=315)                             #Define a Entry and put it in position

        BtnT1 = tk.Button(root, width=15, text='Motor A Turning',fg=color_text,bg=color_btn,relief='ridge')
        BtnT1.place(x=785,y=370)
        E_T1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_T1.place(x=785,y=405)                             #Define a Entry and put it in position

        BtnT2 = tk.Button(root, width=15, text='Motor B Turning',fg=color_text,bg=color_btn,relief='ridge')
        BtnT2.place(x=785,y=460)
        E_T2 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_T2.place(x=785,y=495)                             #Define a Entry and put it in position

        BtnVLC = tk.Button(root, width=15, text='VLC Path',fg=color_text,bg=color_btn,relief='ridge')
        BtnVLC.place(x=785,y=550)
        E_VLC = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
        E_VLC.place(x=785,y=585)                             #Define a Entry and put it in position

        E_C1.insert ( 0, 'Default:425' ) 
        E_C2.insert ( 0, 'Default:425' ) 
        E_M1.insert ( 0, 'Default:100' ) 
        E_M2.insert ( 0, 'Default:100' )
        E_T1.insert ( 0, 'Default:30' ) 
        E_T2.insert ( 0, 'Default:30' )
        E_VLC.insert ( 0, '%s'%import_path('addr:') )  

        def ipcon(event):
            global ipcon
            if ipcon == 0:
                print('set up video server')
                BtnIP.config(state='disabled')
                ipcon=1
                vs=thread.Thread(target=video_show)   #Define a thread for video stream receiving
                vs.setDaemon(True)                    #'True' means it is a front thread,it would close when the mainloop() closes
                vs.start()                            #Thread starts
                ip_send_thread=thread.Thread(target=ip_send)
                ip_send_thread.setDaemon(True)
                ip_send_thread.start()

        def spd_set():                 #Call this function for speed adjustment
            tcpClicSock.send(('spdset:%s'%var_spd.get()).encode())   #Get a speed value from IntVar and send it to the car
            l_ip_2.config(text='Speed:%s'%var_spd.get())             #Put the speed value on the speed status label

        def EC1_set(event):            #Call this function for speed adjustment
            tcpClicSock.send(('EC1set:%s'%E_C1.get()).encode())   #Get a speed value from IntVar and send it to the car

        def EC2_set(event):            #Call this function for speed adjustment
            tcpClicSock.send(('EC2set:%s'%E_C2.get()).encode())   #Get a speed value from IntVar and send it to the car

        def EM1_set(event):            #Call this function for speed adjustment
            tcpClicSock.send(('EM1set:%s'%E_M1.get()).encode())   #Get a speed value from IntVar and send it to the car

        def EM2_set(event):            #Call this function for speed adjustment
            tcpClicSock.send(('EM2set:%s'%E_M2.get()).encode())   #Get a speed value from IntVar and send it to the car

        def ET1_set(event):            #Call this function for speed adjustment
            tcpClicSock.send(('ET1set:%s'%E_T1.get()).encode())   #Get a speed value from IntVar and send it to the car

        def ET2_set(event):            #Call this function for speed adjustment
            tcpClicSock.send(('ET2set:%s'%E_T2.get()).encode())   #Get a speed value from IntVar and send it to the car

        def VLC_set(event):       #Call this function to save a new VLC path
            new_path=E_VLC.get()
            if len(new_path) > 7:
                replace_path('addr:',new_path)

        def connect(event):       #Call this function to connect with the server
            if ip_stu == 1:
                sc=thread.Thread(target=socket_connect) #Define a thread for connection
                sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
                sc.start()                              #Thread starts

        def connect_2():          #Call this function to connect with the server
            if ip_stu == 1:
                sc=thread.Thread(target=socket_connect) #Define a thread for connection
                sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
                sc.start()                              #Thread starts

        def socket_connect():     #Call this function to connect with the server
            global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr
            ip_adr=E1.get()       #Get the IP address from Entry

            if ip_adr == '':      #If no input IP address in Entry,import a default IP
                ip_adr=num_import('IP:')
                l_ip_4.config(text='Connecting')
                l_ip_4.config(bg='#FF8F00')
                l_ip_5.config(text='Default:%s'%ip_adr)
                E1.insert ( 0, '%s'%ip_adr ) 
                pass
            
            SERVER_IP = ip_adr
            SERVER_PORT = 10223   #Define port serial 
            BUFSIZ = 1024         #Define buffer size
            ADDR = (SERVER_IP, SERVER_PORT)
            tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

            for i in range (1,6): #Try 5 times if disconnected
                try:
                    if ip_stu == 1:
                        print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
                        print("Connecting")
                        tcpClicSock.connect(ADDR)        #Connection with the server
                    
                        print("Connected")
                    
                        l_ip_5.config(text='IP:%s'%ip_adr)
                        l_ip_4.config(text='Connected')
                        l_ip_4.config(bg='#558B2F')

                        replace_num('IP:',ip_adr)
                        E1.config(state='disabled')      #Disable the Entry
                        Btn14.config(state='disabled')   #Disable the Entry
                        BtnIP.config(state='normal')
                    
                        ip_stu=0                         #'0' means connected
                    
                        at=thread.Thread(target=code_receive) #Define a thread for data receiving
                        at.setDaemon(True)                    #'True' means it is a front thread,it would close when the mainloop() closes
                        at.start()                            #Thread starts
                        ipaddr=tcpClicSock.getsockname()[0]
                        break
                    else:
                        break
                except Exception:
                    print("Cannot connecting to server,try it latter!")
                    l_ip_4.config(text='Try %d/5 time(s)'%i)
                    l_ip_4.config(bg='#EF6C00')
                    print('Try %d/5 time(s)'%i)
                    ip_stu=1
                    time.sleep(1)
                    continue
            if ip_stu == 1:
                l_ip_4.config(text='Disconnected')
                l_ip_4.config(bg='#F44336')

        def code_receive():     #A function for data receiving
            global ipcon
            while True:
                code_car = tcpClicSock.recv(BUFSIZ) #Listening,and save the data in 'code_car'
                l_ip.config(text=code_car)          #Put the data on the label

                if 'list' in str(code_car):         #Scan result receiving start
                    dis_list=[]
                    f_list=[]
                    list_str=code_car.decode()
                    
                    while  True:                    #Save scan result in dis_list
                        code_car = tcpClicSock.recv(BUFSIZ)
                        if 'finished' in str(code_car):
                            break
                        list_str+=code_car.decode()
                        l_ip.config(text='Scanning')
                    
                    dis_list=list_str.split()       #Save the data as a list
                    l_ip.config(text='Finished')
                    
                    for i in range (0,len(dis_list)):   #Translate the String-type value in the list to Float-type
                        try:
                            new_f=float(dis_list[i])
                            f_list.append(new_f)
                        except:
                            continue
                    
                    dis_list=f_list

                    can_scan_1 = tk.Canvas(root,bg=color_can,height=300,width=740,highlightthickness=0) #define a new canvas
                    can_scan_1.place(x=30,y=90)                                                         #And put it in the same position as the old one

                    x_range = var_x_scan.get()          #Get the value of scan range from IntVar

                    for i in range (0,len(dis_list)):   #Scale the result to the size as canvas
                        try:
                            len_dis_1 = int((dis_list[i]/x_range)*300)                          #600 is the height of canvas
                            pos     = int((i/len(dis_list))*740)                                #740 is the width of canvas
                            pos_ra  = int(((i/len(dis_list))*140)+20)                           #Scale the direction range to (20-160)
                            len_dis = int(len_dis_1*(math.sin(math.radians(pos_ra))))           #len_dis is the height of the line

                            x0_l,y0_l,x1_l,y1_l=pos,(300-len_dis),pos,(300-len_dis)             #The position of line
                            x0,y0,x1,y1=(pos+3),(300-len_dis+3),(pos-3),(300-len_dis-3)         #The position of arc

                            if pos <= 370:                                                      #Scale the whole picture to a shape of sector
                                pos = 370-abs(int(len_dis_1*(math.cos(math.radians(pos_ra)))))
                                x1_l= (x1_l-math.cos(math.radians(pos_ra))*330)
                            else:
                                pos = abs(int(len_dis_1*(math.cos(math.radians(pos_ra)))))+370
                                x1_l= x1_l+abs(math.cos(math.radians(pos_ra))*330)

                            y1_l    = y1_l-abs(math.sin(math.radians(pos_ra))*330)              #Orientation of line

                            line = can_scan_1.create_line(pos,y0_l,x1_l,y1_l,fill=color_line)   #Draw a line on canvas
                            point_scan = can_scan_1.create_oval((pos+3),y0,(pos-3),y1,fill=color_oval,outline=color_oval) #Draw a arc on canvas
                        except:
                            pass

                    line = can_scan_1.create_line(0,75,740,75,fill='darkgray')                #Draw a line on canvas
                    line = can_scan_1.create_line(0,150,740,150,fill='darkgray')                #Draw a line on canvas
                    line = can_scan_1.create_line(0,225,740,225,fill='darkgray')                #Draw a line on canvas

                    arc_1 = can_scan_1.create_arc(185,150,555,450,outline='darkgray',extent=180,style='arc')    #Draw a arc on canvas
                    arc_1 = can_scan_1.create_arc(0,0,740,600,outline='darkgray',extent=180,style='arc')    #Draw a arc on canvas

                    can_tex_11=can_scan_1.create_text((27,217),text='%sm'%round((x_range/4),2),fill='#aeea00')     #Create a text on canvas
                    can_tex_12=can_scan_1.create_text((27,142),text='%sm'%round((x_range/2),2),fill='#aeea00')     #Create a text on canvas
                    can_tex_13=can_scan_1.create_text((27,67),text='%sm'%round((x_range*0.75),2),fill='#aeea00')  #Create a text on canvas
                
                if 'SET' in str(code_car):
                    set_list=code_car.decode()
                    set_list=set_list.split()
                    s1,s2,s3,s4,s5,s6=set_list[1:]
                    E_C1.delete(0,50)
                    E_C2.delete(0,50)
                    E_M1.delete(0,50)
                    E_M2.delete(0,50)
                    E_T1.delete(0,50)
                    E_T2.delete(0,50)

                    E_C1.insert ( 0, '%d'%int(s1) ) 
                    E_C2.insert ( 0, '%d'%int(s2) ) 
                    E_M1.insert ( 0, '%d'%int(s3) ) 
                    E_M2.insert ( 0, '%d'%int(s4) )
                    E_T1.insert ( 0, '%d'%int(s5) ) 
                    E_T2.insert ( 0, '%d'%int(s6) )

                elif '1' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Moving Forward')   #Put the text on the label
                elif '2' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Moving Backward')  #Put the text on the label
                elif '3' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Turning Left')     #Put the text on the label
                elif '4' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Turning Right')    #Put the text on the label
                elif '5' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Look Up')          #Put the text on the label
                elif '6' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Look Down')        #Put the text on the label
                elif '7' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Look Left')        #Put the text on the label
                elif '8' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Look Right')       #Put the text on the label
                elif '9' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Stop')             #Put the text on the label
                elif '0' in str(code_car):               #Translate the code to text
                    l_ip.config(text='Auto Mode On')     #Put the text on the label
                elif 'video_off' in str(code_car):
                    BtnIP.config(state='normal')
                    ipcon=0


        s1 = tk.Scale(root,label="               < Slow   Speed Adjustment   Fast >",
        from_=0.4,to=1,orient=tk.HORIZONTAL,length=400,
        showvalue=0.1,tickinterval=0.1,resolution=0.2,variable=var_spd,fg=color_text,bg=color_bg,highlightthickness=0)
        s1.place(x=200,y=400)                            #Define a Scale and put it in position

        s2 = tk.Scale(root,label="< Near   Scan Range Adjustment(Meter(s))   Far >",
        from_=1,to=5,orient=tk.HORIZONTAL,length=300,
        showvalue=1,tickinterval=1,resolution=1,variable=var_x_scan,fg=color_text,bg=color_bg,highlightthickness=0)
        s2.place(x=390,y=0)                              #Define a Scale and put it in position

        l_ip=tk.Label(root,width=18,text='Status',fg=color_text,bg=color_btn)
        l_ip.place(x=30,y=410)                           #Define a Label and put it in position

        l_ip_2=tk.Label(root,width=18,text='Speed:%s'%(var_spd.get()),fg=color_text,bg=color_btn)
        l_ip_2.place(x=30,y=445)                         #Define a Label and put it in position

        l_ip_4=tk.Label(root,width=18,text='Disconnected',fg=color_text,bg='#F44336')
        l_ip_4.place(x=637,y=410)                         #Define a Label and put it in position

        l_ip_5=tk.Label(root,width=18,text='Use default IP',fg=color_text,bg=color_btn)
        l_ip_5.place(x=637,y=445)                         #Define a Label and put it in position

        l_inter=tk.Label(root,width=45,text='< Car Adjustment              Camera Adjustment>\nW:Move Forward                 Look Up:I\nS:Move Backward            Look Down:K\nA:Turn Left                          Turn Left:J\nD:Turn Right                      Turn Right:L\nZ:Auto Mode On          Look Forward:H\nC:Auto Mode Off      Ultrasdonic Scan:X' ,
        fg='#212121',bg='#90a4ae')
        l_inter.place(x=240,y=480)                       #Define a Label and put it in position

        E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
        E1.place(x=170,y=40)                             #Define a Entry and put it in position

        l_ip_3=tk.Label(root,width=10,text='IP Address:',fg=color_text,bg='#000000')
        l_ip_3.place(x=165,y=15)                         #Define a Label and put it in position

        Btn14= tk.Button(root, width=8, text='Connect',fg=color_text,bg=color_btn,command=connect_2,relief='ridge')
        Btn14.place(x=300,y=35)                          #Define a Button and put it in position

        #Define buttons and put these in position
        Btn0 = tk.Button(root, width=8, text='Forward',fg=color_text,bg=color_btn,relief='ridge')
        Btn1 = tk.Button(root, width=8, text='Backward',fg=color_text,bg=color_btn,relief='ridge')
        Btn2 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
        Btn3 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')
        Btn4 = tk.Button(root, width=8, text='Auto OFF',fg=color_text,bg=color_btn,relief='ridge')
        Btn5 = tk.Button(root, width=8, text='Auto',fg=color_text,bg=color_btn,relief='ridge')
        
        Btn6 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
        Btn7 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')
        Btn8 = tk.Button(root, width=8, text='Down',fg=color_text,bg=color_btn,relief='ridge')
        Btn9 = tk.Button(root, width=8, text='Up',fg=color_text,bg=color_btn,relief='ridge')
        Btn10 = tk.Button(root, width=8, text='Home',fg=color_text,bg=color_btn,relief='ridge')
        Btn11 = tk.Button(root, width=8, text='Exit',fg=color_text,bg=color_btn,relief='ridge')

        Btn12 = tk.Button(root, width=8, text='Set',command=spd_set,fg=color_text,bg=color_btn,relief='ridge')
        Btn13 = tk.Button(root, width=8, text='Scan',fg=color_text,bg=color_btn,relief='ridge')

        BtnIP = tk.Button(root, width=8, text='Video',fg=color_text,bg=color_btn,relief='ridge',state='disabled')

        BtnIP.place(x=100,y=575)
        Btn0.place(x=100,y=495)
        Btn1.place(x=100,y=530)
        Btn2.place(x=30,y=530)
        Btn3.place(x=170,y=530)
        Btn4.place(x=170,y=575)
        Btn5.place(x=30,y=575)
        
        Btn6.place(x=565,y=530)
        Btn7.place(x=705,y=530)
        Btn8.place(x=635,y=565)
        Btn9.place(x=635,y=495)
        Btn10.place(x=635,y=530)
        Btn11.place(x=705,y=10)

        Btn12.place(x=535,y=407)
        Btn13.place(x=705,y=45)


        # Bind the buttons with the corresponding callback function
        BtnIP.bind('<ButtonPress-1>', ipcon)
        Btn0.bind('<ButtonPress-1>', call_forward)
        Btn1.bind('<ButtonPress-1>', call_back)
        Btn2.bind('<ButtonPress-1>', call_Left)
        Btn3.bind('<ButtonPress-1>', call_Right)
        Btn4.bind('<ButtonPress-1>', call_Stop)
        Btn5.bind('<ButtonPress-1>', call_auto)
        Btn6.bind('<ButtonPress-1>', call_left)
        Btn7.bind('<ButtonPress-1>', call_right)

        Btn8.bind('<ButtonPress-1>', call_under)
        Btn9.bind('<ButtonPress-1>', call_on)
        Btn10.bind('<ButtonPress-1>', call_home)
        Btn11.bind('<ButtonPress-1>', call_exit)
        Btn13.bind('<ButtonPress-1>', scan)

        Btn0.bind('<ButtonRelease-1>', call_stop)
        Btn1.bind('<ButtonRelease-1>', call_stop)
        Btn2.bind('<ButtonRelease-1>', call_stop)
        Btn3.bind('<ButtonRelease-1>', call_stop)
        Btn4.bind('<ButtonRelease-1>', call_stop)

        BtnC1.bind('<ButtonPress-1>', EC1_set)
        BtnC2.bind('<ButtonPress-1>', EC2_set)
        BtnM1.bind('<ButtonPress-1>', EM1_set)
        BtnM2.bind('<ButtonPress-1>', EM2_set)
        BtnT1.bind('<ButtonPress-1>', ET1_set)
        BtnT2.bind('<ButtonPress-1>', ET2_set)
        BtnVLC.bind('<ButtonPress-1>', VLC_set)
        # Bind the keys with the corresponding callback function
        root.bind('<KeyPress-w>', call_forward) 
        root.bind('<KeyPress-a>', call_Left)
        root.bind('<KeyPress-d>', call_Right)
        root.bind('<KeyPress-s>', call_back)

        # When these keys is released,call the function call_stop()
        root.bind('<KeyRelease-w>', call_stop)
        root.bind('<KeyRelease-a>', call_stop)
        root.bind('<KeyRelease-d>', call_stop)
        root.bind('<KeyRelease-s>', call_stop)

        root.bind('<KeyRelease-v>', ipcon)

        # Press these keyss to call the corresponding function()
        root.bind('<KeyPress-c>', call_Stop)
        root.bind('<KeyPress-z>', call_auto) 
        root.bind('<KeyPress-j>', call_left)
        root.bind('<KeyPress-l>', call_right)
        root.bind('<KeyPress-h>', call_home)
        root.bind('<KeyPress-k>', call_under)
        root.bind('<KeyPress-i>', call_on)
        root.bind('<KeyPress-x>', scan)
        root.bind('<Return>', connect)
        root.bind('<Shift_L>',call_stop)
        
        global stat
        if stat==0:              # Ensure the mainloop runs only once
                root.mainloop()  # Run the mainloop()
                stat=1           # Change the value to '1' so the mainloop() would not run again.

if __name__ == '__main__':
    try:
        loop()                   # Load GUI
    except KeyboardInterrupt:
        tcpClicSock = socket(AF_INET, SOCK_STREAM) # Define socket for future socket-closing operation
    tcpClicSock.close()          # Close socket or it may not connect with the server again
    player.terminate()
