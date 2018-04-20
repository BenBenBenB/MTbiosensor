
from time import sleep

import numpy as np

from Phidget22.Devices.Stepper import Stepper
from lucam import Lucam

class Biosensor():

    def __init__(self):
        self.stepper = BioStepper()
        self.camera = BioCam(1)
        self.image = self.take_picture()
        # Connect to stepper motor
        self.stepper.openWaitForAttachment(5000)

        #initialize stepper movement values
        self.stepper.setEngaged(True)
        self.stepper.setAcceleration(87543)
        self.stepper.setVelocityLimit(8000)
        self.stepper.setCurrentLimit(0.5)
        sleep(.5)

    def take_picture(self):
        return self.camera.TakeSnapshot()

    def save_image(self, image, filename):
        self.camera.SaveImage(image,filename)

    def take_scan(self, width, rows, spacing):
        for i in range(rows):
            #Take picture
            print("Taking picture %d at position %d um"% (i+1,self.stepper.pos))
            image = self.take_picture()
            sleep(.5)
            #Save
            self.save_image(image,'pics\\test%d.tif'% (i+1))
            #Move
            self.stepper.move(spacing)
            sleep(.5)

    def interpret_image(self, image, width):
        pass


    # Move back to home position and disengage stepper motor
    def stop(self):
        # Move stepper back to home and turn of stepper
        self.camera.CameraClose()
        self.stepper.move_to(0)
        self.stepper.setEngaged(False)
        sleep(1)
        self.stepper.close()
        
class BioStepper(Stepper):
    
    def __init__(self,pos = 0,scale = .6085):
        super().__init__() # call parent init
        # self.index = 0  #i'd use this if I was not lazy
        self.pos = pos      # micrometers
        self.SCALE = scale  # steps/micrometer
        self.MINPOS = -2000 # steps
        self.MAXPOS = 30000 # steps

    # Move the slide left or right by an amount of micrometers.
    def move(self, amount):
        # get target, in steps
        target = int((self.pos + amount)*self.SCALE)
        if self.inbounds(target):
            self.setEngaged(True)
            self.setTargetPosition(target)
            while self.getPosition() != target:
                pass
            self.setEngaged(False)
            self.pos += amount
        else:
            print("out of bounds")

    # Move to a new position given in micrometers
    def move_to(self, newpos):
        # get target in steps
        target = int(newpos*self.SCALE)
        if self.inbounds(target):
            self.setEngaged(True)
            self.setTargetPosition(target)
            while self.getPosition() != target:
                pass
            self.setEngaged(False)
            self.pos = newpos
        else:
            pass #idk, raise an exception or something
        


    #Returns whether a position is valid or not
    def inbounds(self, position):
        return (self.MINPOS <= position <= self.MAXPOS)


class BioCam(Lucam):
    
    def __init__(self, number=1):
        super().__init__(number=1) #call parent init
