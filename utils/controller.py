from subprocess import Popen
import os
import subprocess
from tkinter import StringVar, Toplevel, Label

from models.config import Config
from pages.main_menu import MainMenu
from pages.settings import Settings

class Controller():
	def __init__(self, container, app_context):

		self.config = Config()
		self.app = app_context

		# Create frames for other menus. This allows us to switch between them
		self.frames = {}
		for F in (MainMenu, Settings):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky='nsew')

		if self.config.is_dirs_valid():
			self.show_frame('MainMenu')
		else:
			self.show_frame('Settings')

	def show_frame(self, page_name):
		'''Shows frame by its name'''
		frame = self.frames[page_name]
		self.set_window_size(frame.window_size[0], frame.window_size[1])
		frame.tkraise()

	def render_video(self):
		if not self.config.replay_path:
			print('No replay file')
			return

		# Create waiting window
		new_window = Toplevel(self.app)
		new_window.title("Video is rendering!")
		new_window.geometry("600x400")
		self.app.eval(f'tk::PlaceWindow {str(new_window)} center')

		out_text = StringVar()
		label = Label(new_window, textvariable=out_text, width=600)
		label.grid(row=0, column=0)
		label.pack()

		new_window.tkraise()
		new_window.update_idletasks()
		p = Popen(f'danser -quickstart \
			-skin="{self.config.skin_name.get()}" \
			-replay="{self.config.replay_path}" \
			-record', shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		# Create render output to tkinter window
		out = 'start'
		while not "Finished" in str(out):
			out = p.stdout.readline()
			print(out)
			out_text.set(out)
			if "Finished" in str(out):
				break
			new_window.update()
			
		new_window.destroy()

	def open_videos_folder(self):
		_str = "start danser\\videos"
		os.system(_str)

	def set_window_size(self, width, height):
		self.app.geometry(f'{width}x{height}')
		self.app.minsize(width, height)
		self.app.maxsize(width, height)
