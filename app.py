from tkinter import *
from tkinter.ttk import *
from os import environ, getcwd

from utils.controller import Controller
from utils.version_check import check_version


class App(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		
		self.geometry('600x100')
		self.eval('tk::PlaceWindow . center')
		self.title('Replay Recorder')

		# Set PATH to danser & ffmpeg
		environ['PATH'] += f';{getcwd()}/ffmpeg;{getcwd()}/danser'

		# Creating main frame
		container = Frame(self)
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		controller = Controller(container, self)


if __name__ == "__main__":
	if not check_version():
		print("You can download new version!")
	app = App()
	app.mainloop()
