import socket
import random
import sys
import time
import re
import tkinter as tk
from tkinter import simpledialog
from threading import Thread

ROOT = tk.Tk()

ROOT.withdraw()


#HOST = "127.0.0.1"  # The server's hostname or IP address
#PORT = 3920  # The port used by the server
HOST = "192.168.3.11"  # The server's hostname or IP address
PORT = 3920  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#Thread running in the background only for sending Alivejog message
def backgroundAlive():
    while True:
            try:
                # send alive message every second
                data = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND";
                s.send(data.encode());          
                time.sleep(1)                
            except:
                print("backgroundAlive_Exception")
                time.sleep(1)

#Thread running in the background only for receiving status message from Server and processing the information
def getResponse():
    
    global moveFlag
    global parts
    moveFlag = False
    
    while True:
            try:
                try:
                    data = s.recv(4096)
                    #print(f"Received {data!r}")
                except BlockingIOError:
                    print("no data")
                
                data = data.decode('ASCII').strip('\r\n')                 
                parts = data.split(' ')
                #print(parts)
                
                global posJointsSetpoint
                global posJointsCurrent
                global posCartesian
                global overrideValue
                global dinValue
                global doutValue
                global emergencyStopStatus
                global supplyVoltage
                global currentAll
                global currentJoint 
                global errorString 
                global errorCode 
                global kinState
                global refInfo
                
                #Store all status message in array of this format
                
                posJointsSetpoint = parts[parts.index("POSJOINTSETPOINT")+1:parts.index("POSJOINTSETPOINT")+7]
                posJointsSetpoint = [round(float(x),1) for x in posJointsSetpoint]
                
                posJointsCurrent = parts[parts.index("POSJOINTCURRENT")+1:parts.index("POSJOINTCURRENT")+7]   
                posJointsCurrent = [round(float(x),1) for x in posJointsCurrent]
                
                posCartesian = parts[parts.index("POSCARTROBOT")+1:parts.index("POSCARTROBOT")+7]
                posCartesian = [round(float(x),1) for x in posCartesian]
                
                overrideValue = parts[parts.index("OVERRIDE")+1:parts.index("OVERRIDE")+2]
                dinValue = parts[parts.index("DIN")+1:parts.index("DIN")+2]
                doutValue = parts[parts.index("DOUT")+1:parts.index("DOUT")+2]
                emergencyStopStatus = parts[parts.index("ESTOP")+1:parts.index("ESTOP")+2]
                supplyVoltage = parts[parts.index("SUPPLY")+1:parts.index("SUPPLY")+2]
                currentAll = parts[parts.index("CURRENTALL")+1:parts.index("CURRENTALL")+2]
                currentJoint = parts[parts.index("CURRENTJOINTS")+1:parts.index("CURRENTJOINTS")+10]
                errorString = parts[parts.index("ERROR")+1:parts.index("ERROR")+2]
                errorCode = parts[parts.index("ERROR")+2:parts.index("ERROR")+18]
                kinState = parts[parts.index("KINSTATE")+1:parts.index("KINSTATE")+2]
                
                if "ReferencingInfo" in parts:
                    refInfo = parts[parts.index("ReferencingInfo"):parts.index("ReferencingInfo")+14]
                
                if "EXECACK" in parts:
                    moveFlag = True
                    
                if "EXECEND" in parts:     
                    moveFlag = False

            except Exception as e:
                errorMsg = e
                #print(errorMsg)


#This function receive 6 argument for Joint movement A1 - A6, send the move command only finished when reach the destination.
def moveCommand(a1, a2, a3, a4, a5, a6):
    
    #Send the move command to the tinyctrl
    data = 'CRISTART 18 CMD Move Joint ' + str(a1) + ' ' + str(a2) + ' ' + str(a3) + ' ' + str(a4) + ' ' + str(a5) + ' ' + str(a6) + ' 0 0 0 ' + '10' + ' CRIEND'
    s.send(data.encode())
                
def moveCommandType(x, y, z, a, b, c,  speed, moveType="Cart"):
    
    data = f'CRISTART 18 CMD Move ' + str(moveType) + str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(a) + ' ' + str(b) + ' ' + str(c) + ' 0 0 0 ' + str(speed) + ' CRIEND'
    s.send(data.encode())

daemon = Thread(target=backgroundAlive, daemon=True, name='Monitor')
daemon.start()
daemon2 = Thread(target=getResponse, daemon=True, name='Monitor')
daemon2.start()
time.sleep(4)
   
while True:

    data = 'CRISTART 1234 CMD Enable CRIEND'
    s.send(data.encode())
    time.sleep(1)

    moveCommand(10.0, 10.0, 10.0, 0.0, 0.0, 0.0)  #A1,A2,A3,A4,A5,A6. if your robot is 3 axis, you may set A4 - A6 as "0.0" 
    time.sleep(1)
    moveCommand(10.0, 15.0, 15.0, 0.0, 0.0, 0.0)
    sys.exit()
        
        