from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.ttk import Progressbar as PB
import subprocess
import os
import re
import threading

from models.config import Config
from pages.main_menu import MainMenu
from pages.settings import Settings

class Controller():
	def __init__(self, container, app_context):
		self.app = app_context
		self.config = Config(self)

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
		if self.config.is_db_loading:
			messagebox.showwarning(title="Warning!", message="Wait for maps to import to database before rendering!\nClose this window to continue import.")
			return
		if not self.config.replay_path:
			print('No replay file')
			return

		# Create waiting window
		new_window = Toplevel(self.app)
		new_window.geometry("600x125")
		self.app.eval(f'tk::PlaceWindow {str(new_window)} center')

		stage = Label(new_window, text='Starting')
		stage.place(x=25, y=10)

		curr_map = Label(new_window, text='', width=580)
		curr_map.place(x=25, y=30)

		progress_bar = PB(new_window, orient=HORIZONTAL, length=550, value=0, maximum=100)
		progress_bar.place(x=25, y=60)

		new_window.tkraise()
		new_window.update_idletasks()
		p = subprocess.Popen(f'danser -quickstart \
			-skin="{self.config.skin_name.get()}" \
			-replay="{self.config.replay_path}" \
			-record', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		
		# Create render output to tkinter window
		output = 'Starting'
		while not 'Finished!' in output:
			output = str(p.stdout.readline())
			if 'New beatmap found:' in output:
				stage.config(text='Scanning for new maps')
				curr_map.config(text=output[58:-1])
			elif 'Imported:' in output:
				stage.config(text='Importing new maps')
				curr_map.config(text=output[49:-8])
			elif 'Progress:' in output:
				stage.config(text='Rendering video')
				progress_bar['value'] = int(re.search("Progress: ([0-9]*)%", output).group(1))
				curr_map.config(text='')
			elif 'Finished!' in output:
				stage.config(text='Finished')	

			print(output)
			new_window.update()

		new_window.destroy()

	def open_videos_folder(self):
		_str = "start danser\\videos"
		os.system(_str)

	def set_window_size(self, width, height):
		self.app.geometry(f'{width}x{height}')
		self.app.minsize(width, height)
		self.app.maxsize(width, height)
