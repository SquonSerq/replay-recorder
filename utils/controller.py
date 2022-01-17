import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import queue
import os
import re

from models.config import Config
from pages.main_menu import MainMenu
from pages.settings import Settings
from utils.db_controller import Db
from utils.read_queue import Render


class Controller():
	def __init__(self, container, app_context):
		self.app = app_context
		self.config = Config(self)
		self.db = Db()

		self.render_list = []
		self.render_queue = queue.Queue()
		self.output_queue = queue.Queue()
		self.render = Render(self.render_queue, self.output_queue)
		self.render.daemon = True
		self.render.start()

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

	def get_beatmap_data(self, beatmap_hash):
		return self.db.get_beatmap_data(beatmap_hash)

	def add_replay_to_render(self, frame, replay_path, selected_skin):
		self.render_list.append({
			'frame': frame,
			'replay_path': replay_path,
			'selected_skin': selected_skin
		})

	def render_video(self):
		if self.config.is_db_loading:
			mb.showwarning(title="Warning!", message="Wait for maps to import to database before rendering!\nClose this window to continue import.")
			return
		if not self.render_list:
			print('No replays')

		for replay_data in self.render_list:
			self.render_queue.put_nowait(replay_data)

		self.render_list = []

	def open_videos_folder(self):
		_str = "start danser\\videos"
		os.system(_str)

	def set_window_size(self, width, height):
		self.app.geometry(f'{width}x{height}')
		self.app.minsize(width, height)
		self.app.maxsize(width, height)
