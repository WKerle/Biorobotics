import time
from Motor import *
import RPi.GPIO as GPIO


# IR01 -> Left
# IR02 -> Middle
# IR03 -> Right

class LineFollower:
    def __init__(self):
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

            if self.LMR == 1:
                # Only left is on -> turn left
                PWM.setMotorModel(1000, 1000, -1000, -1000)
            elif self.LMR == 2:
                # Only middle sensor is on -> full speed!
                PWM.setMotorModel(1000, 1000, 1000, 1000)
            elif self.LMR == 3:
                # Middle and right sensor on
                PWM.setMotorModel(1000, 1000, -1000, -1000)
            elif self.LMR == 4:
                PWM.setMotorModel(-1000, -1000, 1000, 1000)
            elif self.LMR == 5:
                # Left and right sensor on -> fun mode?
                PWM.setMotorModel(1000, 1000, 1000, 1000)
            elif self.LMR == 6:
                PWM.setMotorModel(-1000, -1000, 1000, 1000)
            elif self.LMR == 7:
                # pass
                PWM.setMotorModel(0, 0, 0, 0)


infrared = LineFollower()
# Main program logic follows:
if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0, 0, 0, 0)
