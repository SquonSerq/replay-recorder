from tkinter import *
from tkinter.ttk import *
from subprocess import Popen
import os
import subprocess

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
		new_window.geometry("600x400")
		self.app.eval(f'tk::PlaceWindow {str(new_window)} center')

		stage_text = StringVar()
		stage = Label(new_window, textvariable=stage_text, width=600)
		stage.place(y=100)
		stage.pack()

		curr_map_text = StringVar()
		curr_map = Label(new_window, textvariable=curr_map_text, width=600)
		curr_map.place(y=150)
		curr_map.pack()

		progress_bar = ProgressBar(new_window, orient=HORIZONTAL, lenght=300)
		progress_bar.place(y=200)
		progress_bar.pack()


		new_window.tkraise()
		new_window.update_idletasks()
		p = Popen(f'danser -quickstart \
			-skin="{self.config.skin_name.get()}" \
			-replay="{self.config.replay_path}" \
			-record', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		# Create render output to tkinter window
		output = 'start'
		while not 'Finished' in output:
			output = str(p.stdout.readline())
			if 'New beatmap found:' in output:
				stage_text.set('Scanning for new maps')
				curr_map_text.set(output[49:-8])
			elif 'Imported:' in output:
				stage_text.set(f'Importing new maps')
				curr_map_text.set(output[49:-8])
			elif 'Progress:' in output:
				stage_text.set(f'Rendering video')
				progress_bar['value'] = int(output[30:32])
				curr_map.destroy()
			print(output)
			new_window.update()

		stage_text.set(f'Finished')

	def open_videos_folder(self):
		_str = "start danser\\videos"
		os.system(_str)

	def set_window_size(self, width, height):
		self.app.geometry(f'{width}x{height}')
		self.app.minsize(width, height)
		self.app.maxsize(width, height)
