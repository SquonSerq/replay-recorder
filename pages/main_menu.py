import tkinter as tk
import tkinter.ttk as ttk
from os import listdir

from utils.colors import *


class MainMenu(ttk.Frame):
	def __init__(self, parent, controller):

		ttk.Frame.__init__(self, parent)
		self.controller = controller
		self.window_size = (800, 600)

		def choose_replay():
			file = tk.filedialog.askopenfile()
			if file:
				self.controller.config.replay_path = file.name
		
		def update_skin_selector(event):
			if self.controller.config.is_dirs_valid():
				skin_selector['menu'].delete(0, 'end')
				for item in listdir(self.controller.config.danser_config['General']['OsuSkinsDir']):
					skin_selector['menu'].add_command(label=item, command=tk._setit(self.controller.config.skin_name, item))


		# Interface to choose skin
		top_menu = tk.Frame(self, height=100)
		top_menu.pack(side=tk.TOP, fill=tk.X)

		top_menu_settings = tk.Frame(top_menu, height=20, **frame_nqb_bg_style)
		top_menu_settings.pack(side=tk.TOP, fill=tk.X)
		top_menu_settings.pack_propagate(0)
		tk.Button(top_menu_settings, text='Settings', command=lambda: controller.show_frame('Settings'), **button_style).pack(side=tk.RIGHT)

		top_menu_skin = tk.Frame(top_menu,  height=80, **frame_db_bg_style)
		top_menu_skin.pack(side=tk.TOP, fill=tk.X)
		top_menu_skin.pack_propagate(0)
		tk.Label(top_menu_skin, text='Selected skin', width=20).pack(side=tk.LEFT, padx="25")

		skin_list = ['default']
		self.controller.config.skin_name.set(skin_list[0])
		if self.controller.config.is_dirs_valid():
			for item in listdir(self.controller.config.danser_config['General']['OsuSkinsDir']):
				skin_list.append(item)

		skin_selector = ttk.OptionMenu(top_menu_skin, self.controller.config.skin_name, *skin_list)
		skin_selector.bind('<1>', update_skin_selector)
		skin_selector.pack(side=tk.LEFT)

		# Frame for control buttons and render queue
		middle_frame = tk.Frame(self, height=500)
		middle_frame.pack(side=tk.TOP, fill=tk.X)

		middle_frame_settings = tk.Frame(middle_frame, height=20, **frame_nqb_bg_style)
		middle_frame_settings.pack(side=tk.TOP, fill=tk.X)
		middle_frame_settings.pack_propagate(0)
		middle_frame_settings.columnconfigure((0, 1, 2), weight=1)
		tk.Button(middle_frame_settings, text='Add replay', command=lambda: choose_replay(), **button_style).grid(row=0, column=0)
		tk.Button(middle_frame_settings, text='Render video', command=lambda: controller.render_video(), **button_style).grid(row=0, column=1)
		tk.Button(middle_frame_settings, text="Open videos folder", command=lambda: controller.open_videos_folder(), **button_style).grid(row=0, column=2)
		
		replays_frame = tk.Frame(middle_frame, height=480, **frame_db_bg_style)
		replays_frame.pack(side=tk.TOP, fill=tk.X)
		middle_frame_settings.pack_propagate(0)
