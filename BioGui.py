#Basic imports
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

class BioGui:

    def __init__(self, master, biosensor):
        #self.img = ImageTk.PhotoImage(Image.open("test30.tif")) #temp
        # This will put controls on the left side and an image on the right side
        # by using the grid geometry manager of tkinter.
        # Colum 0 will be input/controls and column 1 will be image.
        self.m = Frame(master)
        self.m.grid()

        # The image 
        self.display = PictureFrame(self.m, biosensor)
        self.display.frame.grid(row=0,column=1,rowspan=5,sticky=E)

        # Stepper Controls
        self.stepper_controls = StepperControlWidget(self.m, biosensor.stepper, self.display)
        self.stepper_controls.frame.grid(row=0,column=0,sticky=W)

        # input variables.
        # Access with self.input_variables.name.get()
        self.input_variables = InputVariableWidget(self.m)
        self.input_variables.frame.grid(row=1,column=0,sticky=W)



        self.scan_controls = ScanControlWidget(self.m,biosensor,self.display, self.input_variables)
        self.scan_controls.frame.grid(row=2,column=0,sticky = W)

# This class will create a widget used for the input of variables.
class InputVariableWidget:

    def __init__(self, master):

        # Create the whole frame to be added
        self.frame = Frame(master)
        self.frame.grid()
        # Create each input box and pack
        # Knowing that the scanner scans one row at a time:
        #   Width is number of samples in a row
        #   Rows is number of Rows
        #   spacing is space between adjacent samples
        # Access these values with .get()
        # e.g. self.width.get()
        self.width = IntVar()
        self.rows = IntVar()
        self.spacing = DoubleVar()

        # Setting the initial values to what I expect them to be
        self.width.set(50)
        self.rows.set(40)
        self.spacing.set(400)

        # Adding each component to the widget
        Label(self.frame, text="Input Variables:").grid(row=0,sticky=W,columnspan=3)

        Label(self.frame, text="Width:").grid(row=1,sticky=W)
        self.width_entry = Entry(
            self.frame, textvariable=self.width)
        self.width_entry.grid(row=1,column=1)

        Label(self.frame, text="Rows:").grid(row=2,sticky=W)
        self.row_entry = Entry(
            self.frame, textvariable=self.rows)
        self.row_entry.grid(row=2,column=1)

        Label(self.frame, text="Spacing:").grid(row=3,sticky=W)
        self.spacing_entry = Entry(
            self.frame, textvariable=self.spacing)
        self.spacing_entry.grid(row=3,column=1)
        Label(self.frame, text="micrometers").grid(row=3,column=3)


class StepperControlWidget:

    def __init__(self, master, stepper, display):

        # save stepper and display object
        self.stepper = stepper
        self.display = display
        # Create the whole frame to be added
        self.frame = Frame(master)
        self.frame.grid()

        Label(self.frame, text="Stepper Motor Controls:").grid(row=0,columnspan=5,sticky=W)
        # Buttons to move left or right by set amounts and also go home
        Button(self.frame, text="-1000", command=lambda: self.move(-1000)).grid(row=1,column=0,sticky=E)
        Button(self.frame, text=" -100", command=lambda: self.move(-100)).grid(row=1,column=1,sticky=E)
        Button(self.frame, text="Home", command=lambda: self.move_to(0)).grid(row=1,column=2,sticky=E)
        Button(self.frame, text="  100", command=lambda: self.move(100)).grid(row=1,column=3,sticky=E)
        Button(self.frame, text=" 1000", command=lambda: self.move(1000)).grid(row=1,column=4,sticky=E)

        # A text field and button that executes the move_to command when pressed.
        self.target = DoubleVar()
        self.target.set(0)
        Entry(self.frame, textvariable=self.target).grid(row=2,column=0,columnspan=4)
        Button(self.frame, text="Go To", command=lambda: self.move_to(self.target.get())).grid(row=2,column=4,sticky=E)

        # A display of the current position:
        Label(self.frame, text="Current Position: ").grid(row = 3,columnspan=3,sticky=W)
        self.pos_display = Label(self.frame, text=str(self.stepper.pos))
        self.pos_display.grid(row=3,column=3,columnspan=2)

    def move(self, amount):
        self.stepper.move(amount)
        self.display.update_image()
        self.update_pos_display()


    def move_to(self, pos):
        self.stepper.move_to(pos)
        self.display.update_image()
        self.update_pos_display()

    def update_pos_display(self):
        self.pos_display.configure(text=str(self.stepper.pos))

class PictureFrame:

    def __init__(self, master, biosensor):

        # save stepper object
        self.biosensor = biosensor
        # Create the whole frame to be added
        self.frame = Frame(master)
        self.frame.grid()

        self.biosensor.image = self.biosensor.take_picture()
        self.img = ImageTk.PhotoImage(Image.fromarray(self.biosensor.image, 'L'))
        self.display = Label(self.frame, text="camera display", image = self.img)
        self.display.grid()

    def update_image(self):
        self.biosensor.image = self.biosensor.take_picture()
        self.img = ImageTk.PhotoImage(Image.fromarray(self.biosensor.image, 'L'))
        self.display.configure(image = self.img)


# A widget to contain commands to update the image, run scans,
class ScanControlWidget:
    # display is included in initialization to allow update of image shown
    def __init__(self, master, biosensor, display, input_variables):
        self.biosensor = biosensor
        self.display = display
        self.input = input_variables
        self.frame = Frame(master)

        Label(self.frame, text="Scan Controls:").grid(sticky=W)
        b1 = Button(self.frame, text="Update Image", command=display.update_image, width=20)
        b2 = Button(self.frame, text="Save Image", command=self.save_image, width=20)
        b3 = Button(self.frame, text="Run Scan", command=self.run_scan, width=20)

        b1.grid(row=1,column=0,sticky=W)
        b2.grid(row=2,column=0,sticky=W)
        b3.grid(row=3,column=0,sticky=W)

    def run_scan(self):
        self.biosensor.take_scan(self.input.width.get(), self.input.rows.get(), self.input.spacing.get())

    def save_image(self):
        image = self.biosensor.take_picture()
        file = filedialog.asksaveasfilename(defaultextension=".tif")
        if file:
            self.biosensor.save_image(image,file)

        #self.biosensor.save_image(filename)
