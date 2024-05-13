
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
from controller import robot


ROOT = tk.Tk()

ROOT.withdraw()


#HOST = "127.0.0.1"  # The server's hostname or IP address
#PORT = 3920  # The port used by the server
HOST = "192.168.3.11"  # The server's hostname or IP address
PORT = 3920  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
output = []
moveFlag = True
cmdCnt = 1

rebel = robot.RobotRebel(s, moveFlag, cmdCnt)

daemon = Thread(target=rebel.writeLoop, daemon=True, name='Monitor')
daemon.start()
daemon = Thread(target=rebel.readLoop, daemon=True, name='Monitor')
daemon.start()


while True:
    
    #user dialog box
    inputCode = simpledialog.askstring(title="Robot Testing Menu",
                                      prompt="Input:\n1 - Move to position 1\n2 - Move to position 2\n3 - Enable Robot\n4 - Reset Robot\n5 - GetRefInfo\n6 - Display Status Message\n7 - Reference J1\n8 - Reference J2\n9 - Reference J3")    
    #Sending the coordinate for position 1
    if inputCode == "1":
        rebel.moveCommand(20.0, 10.0, 20.0, 0.0, 10.0, 0.0, 10, 'Joint')  #A1,A2,A3,A4,A5,A6. if your robot is 3 axis, you may set A4 - A6 as "0.0"      
        # rebel.moveCommand(15.0, 15.0, 15.0, 10.0, 0.0, 0.0, 20, 'Joint')
        rebel.moveCommand(45.0, 55.0, 15.0, 0.0, 0.0, 0.0, 20, 'Joint')
        rebel.moveCommand(20.0, 10.0, 20.0, 0.0, 10.0, 0.0, 10, 'Joint')
        # rebel.moveCommand(15.0, 15.0, 40.0, 30.0, 40.0, 0.0, 70, 'Joint')
        
    #Sending the coordinate for position 2 
    if inputCode == "2":
        rebel.moveCommand(5.0, 5.0, 5.0, 0.0, 0.0, 0.0, 10, 'Joint')  #A1,A2,A3,A4,A5,A6. if your robot is 3 axis, you may set A4 - A6 as "0.0" 
        time.sleep(1)   
        
    #Sending command to enable to robot
    if inputCode == "3":
        rebel.enable()
        
    #Sending command to reset the robot
    if inputCode == "4":
        rebel.reset()

    if inputCode == 'x':
        with open("output_v3.txt", "w") as text_file:
            text_file.write(str(output))
        sys.exit()
        
        