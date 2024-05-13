from threading import Thread
import time

class TestingClass:
    def __init__(self, moveFlag, counter):
        self.moveFlag = moveFlag
        self.counter = counter
        
    def cmdRobot(self):
        self.moveFlag = True
        print(f"command robot-{self.counter}")
        while True:
            if self.moveFlag == False:
                break
    
    def aliveJog(self):
        print("alive message")
        time.sleep(0.5)

    def execack(self):
        if self.moveFlag == True:
            # process
            self.out_counter()
            time.sleep(5)
        self.execend()
        
    def execend(self):
        self.moveFlag = False
        
    def out_counter(self):
        self.counter += 1

t = TestingClass(False, 1)
daemonx = Thread(target=t.aliveJog, daemon=True, name='Monitor')
daemonx.start()
daemony = Thread(target=t.execack, daemon=True, name='Monitor')
daemony.start()

while True:
    t.cmdRobot()
    t.cmdRobot()
    t.cmdRobot()
    

