import tkinter.messagebox as mb
import os

from models.config import Config
from pages.main_menu import MainMenu
from pages.settings import Settings
from utils.renderer import Renderer
from utils.dao_db import DaoDB


class Controller():
	def __init__(self, container, app_context):
		self.app = app_context
		self.config = Config(self)
		self.db = DaoDB()

		self.renderer = Renderer()
		self.renderer.daemon = True
		self.renderer.start()

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
	
	def add_replay_to_queue(self, replay_data):
		if self.config.is_db_loading:
			mb.showwarning(title="Warning!", message="Wait for maps to import to database before rendering!\nClose this window to continue import.")
			return

		self.renderer.add_replay_to_queue(replay_data)

	def open_videos_folder(self):
		_str = "start danser\\videos"
		os.system(_str)

	def set_window_size(self, width, height):
		self.app.geometry(f'{width}x{height}')
		self.app.minsize(width, height)
		self.app.maxsize(width, height)
