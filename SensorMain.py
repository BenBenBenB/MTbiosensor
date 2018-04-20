#sensorMain
from time import sleep

from tkinter import *

from Biosensor import Biosensor
from BioGui import BioGui

def main():

	# Create biosensor object
	biosensor = Biosensor()

	try:
		# tkinter stuff
		root = Tk()
		app = BioGui(root, biosensor)
		root.winfo_toplevel().title("Biosensor")
		root.mainloop()

	finally:
		# Safely exit
		biosensor.stop()
		exit(0)

main()
