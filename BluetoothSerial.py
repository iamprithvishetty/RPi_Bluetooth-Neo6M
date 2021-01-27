from serial import Serial
import subprocess

#subprocess.run(["sudo","rfcomm","watch","hci0"])
while True:
    try:
        ser = Serial("/dev/rfcomm0")
        break
    except:
        continue
    

while True:
    try:
        print(ser.readline())
    except:
        try:
            ser.close()
            ser = Serial("/dev/rfcomm0")
        except:
            continue
     
