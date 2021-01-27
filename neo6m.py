from serial import Serial
import time
import string
import pynmea2

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
        gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
        print(gps)

