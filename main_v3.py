
######### PLEASE READ BEFORE USING THIS PROGRAM ########
#Disclaimer: The sample program provided by us is for educational and demonstration purposes only. 
#We do not guarantee its accuracy, reliability, or suitability for any particular purpose. 
#We are not responsible for any damage, loss, or liability that may arise from the use of this program. 
#Users are advised to use the program at their own risk and discretion. 
#We strongly recommend that users thoroughly test the program before using it in any critical or production environment. 
#By using this program, users agree to indemnify and hold us harmless from any claims, damages, or expenses that may arise from its use.

import socket
import sys
import time
import tkinter as tk
from tkinter import simpledialog
from threading import Thread

ROOT = tk.Tk()

ROOT.withdraw()

HOST = "192.168.3.11"  # The server's hostname or IP address
PORT = 3920  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
output = []
moveFlag = True
cmdCnt = 1
#Thread running in the background only for sending Alivejog message
def backgroundAlive():
    while True:
            try:
                # send alive message every second
                data = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"
                s.send(data.encode())          
                time.sleep(1)                
            except:
                print("backgroundAlive_Exception")
                time.sleep(1)

#Thread running in the background only for receiving status message from Server and processing the information
def getResponse():
    while True:
        try:
            try:
                global moveFlag
                global output
                global cmdCnt
                
                data = s.recv(4096)
                data = data.decode('ASCII').strip('\r\n')
                
                EXECACK = "EXECACK"
                EXECEND = "EXECEND"
                
                execAckIndex = data.find(EXECACK)
                execEndIndex = data.find(EXECEND)
                
                if execAckIndex != -1:
                    data.split('\n')
                    moveFlag = True
                    print(data)
                    print(f"move => {moveFlag}")
                if execEndIndex != -1:
                    data.split('\n')
                    moveFlag = False
                    print(data)
                    print(f"move => {moveFlag}")
                print(data)
                cmdCnt = cmdCnt+1
                output.append(data)

            except BlockingIOError:
                print("no data")
                
        except Exception as e:
            errorMsg = e
            print(errorMsg)

#This function receive 6 argument for Joint movement A1 - A6, send the move command only finished when reach the destination.
def moveCommand(a1, a2, a3, a4, a5, a6, speed=10, moveType='Joint'):
    global moveFlag
    global cmdCnt
    data = f'CRISTART {cmdCnt}' + ' ' + 'CMD Move' + ' ' + f'{moveType}' + ' ' + str(a1) + ' ' + str(a2) + ' ' + str(a3) + ' ' + str(a4) + ' ' + str(a5) + ' ' + str(a6) + ' 0 0 0 ' + f'{speed}' + ' CRIEND'
    s.send(data.encode())
    while True:
        if moveFlag == False:
            break

def moveLinearCommand(x, y, z, velmm):
    global moveFlag
    global cmdCnt
    data = f'CRISTART {cmdCnt} PROG {cmdCnt} RELATIVELINEAR {x} {y} {z} {velmm} CRIEND'
    s.send(data.encode())
    while True:
        if moveFlag == False:
            break                 

def digitalOut(pinout=21, enable=False):
    # global moveFlag
    global cmdCnt
    #CRISTART 1234 CMD DOUT 21 true CRIEND
    enable = 'true' if enable == True else 'false'
    data = f'CRISTART {cmdCnt} CMD DOUT' + ' ' + str(pinout) + ' ' + str(enable) + ' ' + 'CRIEND'
    s.send(data.encode())  
    
def enableRobot():
    global cmdCnt
    data = f'CRISTART {cmdCnt} CMD Enable CRIEND'
    s.send(data.encode())
    
def resetRobot():
    global cmdCnt
    data = f'CRISTART {cmdCnt} CMD Reset CRIEND'
    s.send(data.encode())

daemon = Thread(target=backgroundAlive, daemon=True, name='Monitor')
daemon.start()
daemon = Thread(target=getResponse, daemon=True, name='Monitor')
daemon.start()


while True:
    moveCommand(20.0, 10.0, 20.0, 0.0, 10.0, 0.0, 10, 'Joint')  #A1,A2,A3,A4,A5,A6. if your robot is 3 axis, you may set A4 - A6 as "0.0"      
    moveCommand(15.0, 15.0, 15.0, 10.0, 0.0, 0.0, 20, 'Joint')
    digitalOut(21, True)
    moveCommand(45.0, 55.0, 15.0, 0.0, 0.0, 0.0, 30, 'Joint')
    digitalOut(21, False)
    moveCommand(15.0, 15.0, 40.0, 30.0, 40.0, 0.0, 30, 'Joint')
    # save log to file
    with open("output_v3.txt", "w") as text_file:
        text_file.write(str(output))
    sys.exit()
        
        