import time
import RPi.GPIO as GPIO
import string
import pynmea2
from serial import Serial
import bluetooth
import subprocess
from subprocess import Popen,PIPE,STDOUT
from threading import Thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lat=0
lng=0

bluetooth_data =""

Reset_Flag = 0

Motor1_0 = 19
Motor1_1 = 26

Motor2_0 = 20
Motor2_1 = 21

Reset_Button = 17

GPIO.setup(Motor1_0,GPIO.OUT)
GPIO.setup(Motor1_1,GPIO.OUT)
GPIO.setup(Motor2_0,GPIO.OUT)
GPIO.setup(Motor2_1,GPIO.OUT)

GPIO.setup(Reset_Button,GPIO.IN, GPIO.PUD_DOWN)

def Neo_Data():
    global lat,lng
    neo = Serial(port='/dev/ttyAMA0',baudrate=9600,timeout=0.5)

    while True:
        dataout = pynmea2.NMEAStreamReader()
        try:
            newdata=neo.readline().decode('utf-8')
        except:
            continue
        #print(newdata)
        if newdata[0:6] == '$GPRMC':
            newmsg=pynmea2.parse(newdata)
            lat=newmsg.latitude
            lng=newmsg.longitude
            gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
            #print(gps)
    
def receiveMessages():
    global bluetooth_data,Reset_Flag,server_sock,client_sock
    while True:
        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

        port = 1
        server_sock.bind(("",port))
        server_sock.listen(1)

        client_sock,address = server_sock.accept()
        print("Accepted connection from " + str(address))
        p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
        stdout_data = p.communicate(input='discoverable off'.encode())[0]
        while True:
          try:
              data = client_sock.recv(1024)
              bluetooth_data = data
              print("received [%s]" % data)
              
          except:
              break
            
          if Reset_Flag == 1:
                  break
        bluetooth_data = ""
        p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
        stdout_data = p.communicate(input='discoverable on'.encode())[0]
        try:
            client_sock.close()
            server_sock.close()
        except:
            continue

def Reset_Check():
    global Reset_Flag,server_sock,client_sock
    while True:
        if GPIO.input(Reset_Button) == True :
            Reset_Flag=1
            try:
                client_sock.close()
                server_sock.close()
            except:
                continue
        elif GPIO.input(Reset_Button) == False:
            Reset_Flag=0
        time.sleep(0.1)
           
if __name__ == "__main__":
    p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    stdout_data = p.communicate(input='discoverable off'.encode())[0]
    p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
    
    stdout_data = p.communicate(input='discoverable on'.encode())[0]
    Thread_Bluetooth_Data = Thread(target = receiveMessages,args =())
    Thread_Neo_Data = Thread(target = Neo_Data ,args=())
    Thread_Reset_Flag = Thread(target = Reset_Check,args=())
    Thread_Bluetooth_Data.start()
    Thread_Neo_Data.start()
    Thread_Reset_Flag.start()
    while True:
        if bluetooth_data == b'U':
            print("Forward")
            GPIO.output(Motor1_0,True)
            GPIO.output(Motor1_1,False)
            
            GPIO.output(Motor2_0,True)
            GPIO.output(Motor2_1,False)
        elif bluetooth_data == b'D':
            print("Backward")
            GPIO.output(Motor1_0,False)
            GPIO.output(Motor1_1,True)
            
            GPIO.output(Motor2_0,False)
            GPIO.output(Motor2_1,True)
            
        elif bluetooth_data == b'C':
            print("Stop")
            GPIO.output(Motor1_0,False)
            GPIO.output(Motor1_1,False)
            
            GPIO.output(Motor2_0,False)
            GPIO.output(Motor2_1,False)
            
        elif bluetooth_data == b'L':
            print("Left")
            GPIO.output(Motor1_0,False)
            GPIO.output(Motor1_1,True)
            
            GPIO.output(Motor2_0,True)
            GPIO.output(Motor2_1,False)
            
        elif bluetooth_data == b'R':
            print("Left")
            GPIO.output(Motor1_0,True)
            GPIO.output(Motor1_1,False)
            
            GPIO.output(Motor2_0,False)
            GPIO.output(Motor2_1,True)
        else:
            print("Stop")
            GPIO.output(Motor1_0,False)
            GPIO.output(Motor1_1,False)
            
            GPIO.output(Motor2_0,False)
            GPIO.output(Motor2_1,False)  
    
            
    
    