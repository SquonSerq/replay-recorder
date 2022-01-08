from tkinter import Frame, StringVar, Tk
from subprocess import Popen
from json import load, dump
from os import environ, getcwd, path

from pages.main_menu import MainMenu
from pages.pre_settings import PreSettings
from pages.settings import Settings


class App(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		
		self.replay_path = ''
		self.skin_name = StringVar()
		self.geometry('800x600+250+200')
		self.eval('tk::PlaceWindow . center')
		self.title('Replay Recorder')

		# Set PATH to danser & ffmpeg
		environ['PATH'] += f';{getcwd()}/ffmpeg;{getcwd()}/danser'

		# Config load
		if not path.exists('./danser/settings/default.json'):
			Popen('danser')
		with open('./danser/settings/default.json', 'r') as f:
			self.config = load(f)

		# Creating main frame
		container = Frame(self)
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# Create frames for other menus. This allows us to switch between them
		self.frames = {}
		for F in (MainMenu, PreSettings, Settings):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky='nsew')

		if self.is_dirs_valid():
			self.show_frame('MainMenu')
		else:
			self.show_frame('PreSettings')

	def is_dirs_valid(self):
			if self.config['General']['OsuSongsDir']:
				if not path.exists(self.config['General']['OsuSongsDir']):
					print('Wrong song directory')
					return False
			else:
				print('No path to songs directory')
				return False

			if self.config['General']['OsuSkinsDir']:
				if not path.exists(self.config['General']['OsuSkinsDir']):
					print('Wrong path to skins directory')
					return False
			else:
				print('No path to skins directory')
				return False
			return True 

	def save_config(self):
		with open('./danser/settings/default.json', 'w') as f:
			dump(self.config, f)

	def show_frame(self, page_name):
		'''Shows frame by its name'''
		frame = self.frames[page_name]
		frame.tkraise()

app = App()
app.mainloop()
