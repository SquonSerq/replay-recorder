import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from osrparse import parse_replay_file
from os import listdir

from utils.colors import *
from utils.image_loader import *


class MainMenu(tk.Frame):
	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.window_size = (800, 600)

		def choose_replay():
			file = fd.askopenfile()
			if file:
				try:
					replay_data = parse_replay_file(file.name)
				except ValueError:
					# Not replay selected
					return

				replay_popup = tk.Frame(self, width=500, height=250, **frame_dg_bg_style, **frame_border)
				replay_popup.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
				replay_popup.pack_propagate(0)

				replay_popup_titlebar = tk.Frame(replay_popup, height=30, **frame_lg_bg_style)
				replay_popup_titlebar.pack(side=tk.TOP, fill=tk.X)
				replay_popup_titlebar.pack_propagate(0)
				frame_name = tk.Label(replay_popup_titlebar, text='Add replay', **label_lg_style)
				frame_name.pack(side=tk.LEFT, padx=10)
				close_button = tk.Button(replay_popup_titlebar, text='✕', command=replay_popup.destroy, **button_titlebar_style)
				close_button.pack(side=tk.RIGHT)

				loading = tk.Label(replay_popup, text='LOADING', **label_lg_style)
				loading.pack(side=tk.TOP, anchor=tk.CENTER)

				beatmap_data = self.controller.db.get_beatmap_data(replay_data.beatmap_hash)
				print(f'{beatmap_data[0]} - {beatmap_data[1]}[{beatmap_data[2]}].',
				      f'Played by {replay_data.player_name} on {replay_data.timestamp}')
				
				loading.destroy()

				map_info = tk.Frame(replay_popup, height=170, **frame_dg_bg_style)
				map_info.pack(side=tk.TOP, fill=tk.X)
				map_info.pack_propagate(0)
				
				path = '/'.join([self.controller.config.danser_config['General']['OsuSongsDir'], beatmap_data[3]])
				image_tk = ImageLoader(path).get_tkinter_image(160, 90)
				print('Loaded image', self.controller.config.danser_config['General']['OsuSongsDir'] + beatmap_data[3])
				photo = tk.Label(map_info, image=image_tk, **borderless)
				photo.image = image_tk
				photo.pack(side=tk.TOP, pady=10)
				tk.Label(map_info, text=f'Played by {replay_data.player_name} on {replay_data.timestamp}', **borderless, **label_dg_style).pack(side=tk.BOTTOM, fill=tk.BOTH, pady=10)
				tk.Label(map_info, text=f'{beatmap_data[0]} - {beatmap_data[1]} [{beatmap_data[2]}]', **borderless, **label_dg_style).pack(side=tk.BOTTOM, fill=tk.BOTH)

				replay_popup_skin = tk.Frame(replay_popup,  height=50, **frame_lg_bg_style)
				replay_popup_skin.pack(side=tk.TOP, fill=tk.X)
				replay_popup_skin.pack_propagate(0)
				tk.Label(replay_popup_skin, text='Selected skin', **label_lg_style).pack(side=tk.LEFT, padx=25)

				def update_skin_selector(event):
					if self.controller.config.is_dirs_valid():
						skin_selector['menu'].delete(0, 'end')
						for item in listdir(self.controller.config.danser_config['General']['OsuSkinsDir']):
							skin_selector['menu'].add_command(label=item, command=tk._setit(skin_name, item))
				skin_name = tk.StringVar()
				skin_list = ['default']
				skin_name.set(skin_list[0])
				if self.controller.config.is_dirs_valid():
					for item in listdir(self.controller.config.danser_config['General']['OsuSkinsDir']):
						skin_list.append(item)
				
				skin_selector = ttk.OptionMenu(replay_popup_skin, skin_name, *skin_list)
				skin_selector.bind('<1>', update_skin_selector)
				skin_selector.pack(side=tk.LEFT)

				def add_replay_to_list():
					q_frame = tk.Frame(q_replays_frame, width=740, height=100, **frame_lg_bg_style)
					q_frame.pack(side=tk.TOP, pady=5)
					q_frame.pack_propagate(0)

					q_photo = tk.Label(q_frame, image=image_tk, **borderless)
					q_photo.image = image_tk
					q_photo.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

					q_text_frame = tk.Frame(q_frame, **frame_lg_bg_style)
					q_text_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)

					tk.Label(q_text_frame, text=f'{beatmap_data[0]} - {beatmap_data[1]} [{beatmap_data[2]}]', **borderless, **label_lg_style).pack(side=tk.TOP, anchor=tk.W, pady=10)
					tk.Label(q_text_frame, text=f'Played by {replay_data.player_name} on {replay_data.timestamp}', **borderless, **label_lg_style).pack(side=tk.TOP, anchor=tk.W, pady=10)
					
					ttk.Progressbar(q_frame, orient=tk.HORIZONTAL, value=0, maximum=100).pack(side=tk.RIGHT, anchor=tk.NW, padx=10, pady=15)
					self.controller.add_replay_to_queue((q_frame, file.name, skin_name.get()))
					replay_popup.destroy()

				tk.Button(replay_popup_skin, text='Render video', command=lambda: add_replay_to_list(), **button_style_popup).pack(side=tk.RIGHT, padx=25)
		
		# Frame for control buttons and render queue
		background = tk.Frame(self, height=600, **frame_lg_bg_style)
		background.pack(side=tk.TOP, fill=tk.X)
		background.pack_propagate(0)

		frame_with_buttons = tk.Frame(background, height=60, **frame_dg_bg_style)
		frame_with_buttons.pack(side=tk.TOP, fill=tk.X)
		frame_with_buttons.pack_propagate(0)
		tk.Button(frame_with_buttons, text='Add replay', command=lambda: choose_replay(), **button_style).pack(side=tk.LEFT, padx=1)
		tk.Button(frame_with_buttons, text="Open videos folder", command=lambda: controller.open_videos_folder(), **button_style).pack(side=tk.LEFT, padx=1)
		tk.Button(frame_with_buttons, text='Settings', command=lambda: controller.show_frame('Settings'), **button_style).pack(side=tk.RIGHT, padx=1)

		replays_frame = tk.Frame(background, width=800, height=540,  **frame_lg_bg_style)
		replays_frame.pack(side=tk.TOP)
		replays_frame.pack_propagate(0)

		q_replays_labels_frame = tk.Frame(replays_frame, height=30, **frame_lg_bg_style)
		q_replays_labels_frame.pack(side=tk.TOP, fill=tk.X)
		q_replays_labels_frame.pack_propagate(0) 
		tk.Label(q_replays_labels_frame, text='Added replays', **label_lg_style).pack(side=tk.LEFT, anchor=tk.N, padx=35, pady=5)
		tk.Label(q_replays_labels_frame, text='Render progress', **label_lg_style).pack(side=tk.RIGHT, anchor=tk.N, padx=45, pady=5)

		q_replays_frame = tk.Frame(replays_frame, width=750, height=450, **frame_dg_bg_style) 
		q_replays_frame.pack(side=tk.TOP, anchor=tk.CENTER)
		q_replays_frame.pack_propagate(0)
