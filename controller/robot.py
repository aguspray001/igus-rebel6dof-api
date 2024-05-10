import time

class RobotRebel:
    def __init__(self, socket, moveFlag):
        self.socket = socket
        self.moveFlag = moveFlag
    
    def writeLoop(self):
        while True:
            try:
                # send alive message every second
                data = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"
                self.socket.send(data.encode())          
                time.sleep(1)                
            except:
                print("backgroundAlive_Exception")
                time.sleep(1)
    
    def readLoop(self):
        while True:
            try:
                try:
                    data = self.socket.recv(4096)
                    data = data.decode('ASCII').strip('\r\n')
                    
                    EXECACK = "EXECACK"
                    EXECEND = "EXECEND"
                    
                    execAckIndex = data.find(EXECACK)
                    execEndIndex = data.find(EXECEND)
                    
                    if execAckIndex != -1:
                        data.split('\n')
                        self.moveFlag = True
                        print(data)
                        print(f"move => {self.moveFlag}")
                    if execEndIndex != -1:
                        data.split('\n')
                        self.moveFlag = False
                        print(data)
                        print(f"move => {self.moveFlag}")

                except BlockingIOError:
                    print("no data")
                    
            except Exception as e:
                errorMsg = e
                print(errorMsg)
    
    def enable(self):
        data = 'CRISTART 1234 CMD Enable CRIEND'
        self.socket.send(data.encode())

    def reset(self):
        data = 'CRISTART 1234 CMD Reset CRIEND'
        self.socket.send(data.encode())
    
    def moveCommand(self, a1, a2, a3, a4, a5, a6, speed=10, moveType='Joint'):
        data = 'CRISTART 18 CMD Move ' + f'{moveType}' + ' ' + str(a1) + ' ' + str(a2) + ' ' + str(a3) + ' ' + str(a4) + ' ' + str(a5) + ' ' + str(a6) + ' 0 0 0 ' + f'{speed}' + ' CRIEND'
        self.socket.send(data.encode())
        while True:
            print(f"testing ==> {self.moveFlag}")
            if self.moveFlag == False:
                break