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
from subprocess import Popen,PIPE,STDOUT
p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='discoverable off'.encode())[0]
p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='discoverable on'.encode())[0]

def receiveMessages():
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
          print("received [%s]" % data)
      except:
          break
  p= Popen(['bluetoothctl'],stdout=PIPE,stdin=PIPE,stderr=PIPE)
  stdout_data = p.communicate(input='discoverable on'.encode())[0]
  client_sock.close()
  server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("hello!!")
  sock.close()
  
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print(str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    
    
while True: 
    receiveMessages()   