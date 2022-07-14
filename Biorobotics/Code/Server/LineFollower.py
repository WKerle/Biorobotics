import time
from Motor import *
import RPi.GPIO as GPIO


# IR01 -> Left
# IR02 -> Middle
# IR03 -> Right


class LineFollower:
    def __init__(self):
        self.CSB = False
        self.isSetBack = False
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def run(self):
        while True:
            self.LMR = 0x00
            if GPIO.input(self.IR01):
                # Left Sensor On
                self.LMR = (self.LMR | 4)
            if GPIO.input(self.IR02):
                # Middle Sensor On
                self.LMR = (self.LMR | 2)
            if GPIO.input(self.IR03):
                # Right Sensor On
                self.LMR = (self.LMR | 1)
            steer(self.LMR)
            #handleModeSwitch(self.LMR, self)

def steer(mode):
  maxV = 2000
  midV = 1200
  minV = 0
  sL = 0
  sR = 0
  if mode ==0:
    sQ = 0
    #sR = 0
  elif mode ==1:
    sL = maxV
    sR = -midV
    PWM.setMotorModel(sL,sL,sR,sR)
  elif mode ==2:
    sL = maxV
    sR = maxV
    PWM.setMotorModel(sL,sL,sL,sL)
  elif mode ==3:
    sL = -midV
    sR = maxV
    PWM.setMotorModel(sL,sL,sR,sR)
  elif mode ==4:
    sR = maxV
    sL = -midV
    PWM.setMotorModel(sL,sL,sR,sR)
  #elif mode ==5:
  elif mode ==6:
    sL = maxV
    sR = -midV
    PWM.setMotorModel(sL,sL,sR,sR)
  elif mode ==7:
    sQ = 0
    #sR = 0


def handleModeSwitch(mode, self):
    if mode == 1:
        # Only right is on -> turn right
        turnRight()
    elif mode == 2:
        # Only middle sensor is on -> full speed!
        PWM.setMotorModel(2000, 2000, 2000, 2000)
#    elif mode == 3:
        # Middle and right sensor on
#        if (self.CSB):
 #           turnRight()
  #      self.CSB = not (self.CSB)
#turnRight()
    elif mode == 4:
        # only left sensor on -> turn left
        turnLeft()
    elif mode == 5:
        # Left and right sensor on -> fun mode?
        PWM.setMotorModel(1000, 1000, 1000, 1000)
#    elif mode == 6:
        # middle and left sensor on -> turn left
#        if (self.CSB):
 #           turnLeft()
  #      self.CSB = not (self.CSB)
#turnLeft()
    elif mode == 0:
        # pass
#        if(self.CSB):
         setBack(self)
#        PWM.setMotorModel(0, 0, 0, 0)
    elif mode == 7:
        turnLeft()


def turnLeft():
    PWM.setMotorModel(-2500, -2500, 1000, 1000)


def turnRight():
    PWM.setMotorModel(1000, 1000, -2500, -2500)


def setBack(self):
    self.CSB = False
    PWM.setMotorModel(-1500, -1500, 1500, 1500)


infrared = LineFollower()
# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0, 0, 0, 0)
