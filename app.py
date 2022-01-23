import tkinter as tk
from os import environ, getcwd

from utils.colors import *
from utils.controller import Controller
from utils.version_check import check_version
from utils.widgets import DraggableWindow


class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		# Set PATH to danser & ffmpeg
		environ['PATH'] += f';{getcwd()}\\ffmpeg;{getcwd()}\\danser'

		# Creating main frame
		DraggableWindow(self, 800, 600, 'Replay Recorder')
		container = tk.Frame(self)
		container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		controller = Controller(container, self)


if __name__ == "__main__":
	if not check_version():
		print("You can download new version!")
	app = App()
	app.mainloop()
