import sqlite3
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from osrparse import parse_replay_file
from os import listdir

from utils.colors import *


class MainMenu(tk.Frame):
	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.window_size = (800, 600)
		self.db = sqlite3.connect("./danser/danser.db")
		self.cursor = self.db.cursor()

		def choose_replay():
			file = fd.askopenfile()
			if file:
				try:
					replay_data = parse_replay_file(file.name)
				except ValueError:
					# Not replay selected
					return

				self.cursor.execute(f'SELECT artist, title, version, dir||"/"||bg FROM beatmaps WHERE md5 = ?', [(replay_data.beatmap_hash)])
				beatmap_data = self.cursor.fetchall()[0]
				print(f'{beatmap_data[0]} - {beatmap_data[1]}[{beatmap_data[2]}].  Played by {replay_data.player_name} on {replay_data.timestamp}')
				
				replay_popup = tk.Frame(self, width=500, height=250, **frame_dg_bg_style, **frame_border)
				replay_popup.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
				replay_popup.pack_propagate(0)

				replay_popup_titlebar = tk.Frame(replay_popup, height=30, **frame_lg_bg_style)
				replay_popup_titlebar.pack(side=tk.TOP, fill=tk.X)
				replay_popup_titlebar.pack_propagate(0)
				frame_name = tk.Label(replay_popup_titlebar, text='Add replay', **frame_lg_bg_style, fg=light_white)
				frame_name.pack(side=tk.LEFT, padx=10)
				close_button = tk.Button(replay_popup_titlebar, text='✕', command=replay_popup.destroy, **button_titlebar_style)
				close_button.pack(side=tk.RIGHT)

				map_info = tk.Frame(replay_popup, height=170, **frame_dg_bg_style)
				map_info.pack(side=tk.TOP, fill=tk.X)
				map_info.pack_propagate(0)
				
				image = Image.open('/'.join([self.controller.config.danser_config['General']['OsuSongsDir'], beatmap_data[3]]))
				image_tk = ImageTk.PhotoImage(image.resize((160, 90)))
				print('Loaded image', self.controller.config.danser_config['General']['OsuSongsDir'] + beatmap_data[3])
				photo = tk.Label(map_info, image=image_tk, **borderless)
				photo.image = image_tk
				photo.pack(side=tk.TOP, pady=10)
				tk.Label(map_info, text=f'Played by {replay_data.player_name} on {replay_data.timestamp}', **borderless, **frame_dg_bg_style, fg=light_white).pack(side=tk.BOTTOM, fill=tk.BOTH, pady=10)
				tk.Label(map_info, text=f'{beatmap_data[0]} - {beatmap_data[1]} [{beatmap_data[2]}]', **borderless, **frame_dg_bg_style, fg=light_white).pack(side=tk.BOTTOM, fill=tk.BOTH)
				

				replay_popup_skin = tk.Frame(replay_popup,  height=50, **frame_lg_bg_style)
				replay_popup_skin.pack(side=tk.TOP, fill=tk.X)
				replay_popup_skin.pack_propagate(0)
				tk.Label(replay_popup_skin, text='Selected skin', **frame_lg_bg_style, fg=light_white).pack(side=tk.LEFT, padx=25)

				def update_skin_selector(event):
					if self.controller.config.is_dirs_valid():
						skin_selector['menu'].delete(0, 'end')
						for item in listdir(self.controller.config.danser_config['General']['OsuSkinsDir']):
							skin_selector['menu'].add_command(label=item, command=tk._setit(self.controller.config.skin_name, item))

				skin_list = ['default']
				self.controller.config.skin_name.set(skin_list[0])
				if self.controller.config.is_dirs_valid():
					for item in listdir(self.controller.config.danser_config['General']['OsuSkinsDir']):
						skin_list.append(item)
				
				skin_selector = ttk.OptionMenu(replay_popup_skin, self.controller.config.skin_name, *skin_list)
				skin_selector.bind('<1>', update_skin_selector)
				skin_selector.pack(side=tk.LEFT)
				tk.Button(replay_popup_skin, text='Render video', command=lambda: controller.render_video(), **button_style_popup).pack(side=tk.RIGHT, padx=25)

				self.controller.config.replay_path = file.name
		
		# Frame for control buttons and render queue
		background = tk.Frame(self, height=600, **frame_lg_bg_style)
		background.pack(side=tk.TOP, fill=tk.X)
		background.pack_propagate(0)

		frame_with_buttons = tk.Frame(background, height=60, **frame_dg_bg_style)
		frame_with_buttons.pack(side=tk.TOP, fill=tk.X)
		frame_with_buttons.pack_propagate(0)
		tk.Button(frame_with_buttons, text='Add replay', command=lambda: choose_replay(), **button_style).pack(side=tk.LEFT, padx=1)
		tk.Button(frame_with_buttons, text='Render video', command=lambda: controller.render_video(), **button_style).pack(side=tk.LEFT, padx=1)
		tk.Button(frame_with_buttons, text="Open videos folder", command=lambda: controller.open_videos_folder(), **button_style).pack(side=tk.LEFT, padx=1)
		tk.Button(frame_with_buttons, text='Settings', command=lambda: controller.show_frame('Settings'), **button_style).pack(side=tk.LEFT, padx=1)

		replays_frame = tk.Frame(background, height=500, **frame_lg_bg_style)
		replays_frame.pack(side=tk.TOP, fill=tk.X)
