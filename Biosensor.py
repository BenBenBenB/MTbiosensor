
from time import sleep

import numpy as np

from Phidget22.Devices.Stepper import Stepper
from lucam import Lucam

class Biosensor():
    """ Unites the camera and stepper motor in one class

    Loads the BioStepper and BioCam objects and defines relevant
    functions to interact with each one.

    Attributes:
        stepper: the stepper object
        camera: the camera object
        image: current image displayed
    """

    def __init__(self):
        """Initializes class and sets stepper values"""
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
        """Uses camera to take picture and return image"""
        return self.camera.TakeSnapshot()

    def save_image(self, image, filename):
        """Saves an image as specified filename"""
        self.camera.SaveImage(image,filename)

    def take_scan(self, width, rows, spacing):
        """Performs a scan and saves images"""
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
        """To be added in future"""
        pass

    def stop(self):
        """Move back to home position and disengage stepper motor"""
        # Move stepper back to home and turn of stepper
        self.camera.CameraClose()
        self.stepper.move_to(0)
        self.stepper.setEngaged(False)
        sleep(1)
        self.stepper.close()
        
class BioStepper(Stepper):
    """ Interfaces with the stepper motor

    Adds custom functions for movement of the stepper motor and 
    internally keeps track of position.

    Attributes:
        pos: the current stepper position
        SCALE: the conversion rate for steps to micrometers
        MINPOS: Minimum position
        MAXPOS: Maximum position
    """
    def __init__(self,pos = 0,scale = .6085):
        """Initialize variables and call Phidget initializer"""
        super().__init__()  # call parent init
        self.pos = pos      # micrometers
        self.SCALE = scale  # steps/micrometer
        self.MINPOS = -2000 # steps
        self.MAXPOS = 30000 # steps

    def move(self, amount):
        """Move the slide left or right by an amount of micrometers."""
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

    def move_to(self, newpos):
        """Move to a new position given in micrometers"""
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
        
    def inbounds(self, position):
        """Returns whether a position is valid or not"""
        return (self.MINPOS <= position <= self.MAXPOS)


class BioCam(Lucam):
    """ Interfaces with the camera

    Does nothing
    """
    def __init__(self, number=1):
        super().__init__(number=1) #call parent init
