from tkinter import *
from tkinter.ttk import *
from os import path
import subprocess
import json

class Config:
	def __init__(self, controller_context):
		self.controller = controller_context
		self.__is_config_exist = True
		self.is_db_loading = False
		self.replay_path = ''
		self.skin_name = StringVar()
		self.danser_config = {}

		self.load_config()
		self.controller.app.after(100, self.load_database)

		self.settings_vars = {
			"SnakingIn": {
				"setting_name": "Sliders snake in",
				"type": BooleanVar,
				"root": self.danser_config['Objects']['Sliders']['Snaking'],
				"field": "In"
			},
			"SnakingOut": {
				"setting_name": "Sliders snake out",
				"type": BooleanVar,
				"root": self.danser_config['Objects']['Sliders']['Snaking'],
				"field": "Out"
			},
			"CursorRipples": {
				"setting_name": "Waves on cursor click",
				"type": BooleanVar,
				"root": self.danser_config['Cursor'],
				"field": "CursorRipples"
			},
			"ButtonClicks": {
				"setting_name": "Show clicked buttons",
				"type": BooleanVar,
				"root": self.danser_config['Gameplay']['KeyOverlay'],
				"field": "Show"
			},
			"StrainGraph": {
				"setting_name": "Show strain graph",
				"type": BooleanVar,
				"root": self.danser_config['Gameplay']['StrainGraph'],
				"field": "Show"
			},
			"PPCounter": {
				"setting_name": "Show PP counter",
				"type": BooleanVar,
				"root": self.danser_config['Gameplay']['PPCounter'],
				"field": "Show"
			}
		}

		for k, v in self.settings_vars.items():
			root = v["root"]
			obj_type = v["type"]
			field = v["field"]
			v["obj"] = obj_type()
			v["obj"].set(root[field])

	def update_from_frame(self, frame_var, root, field):
		root[field] = frame_var.get()

	def is_dirs_valid(self):
			if self.danser_config['General']['OsuSongsDir']:
				if not path.exists(self.danser_config['General']['OsuSongsDir']):
					print('Wrong song directory')
					return False
			else:
				print('No path to songs directory')
				return False

			if self.danser_config['General']['OsuSkinsDir']:
				if not path.exists(self.danser_config['General']['OsuSkinsDir']):
					print('Wrong path to skins directory')
					return False
			else:
				print('No path to skins directory')
				return False
			return True 

	def load_database(self):
		self.is_db_loading = True
		p = subprocess.Popen(f'danser -md5 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

		# Create db import window
		new_window = Toplevel(self.controller.app)
		new_window.title("Importing maps to database")
		new_window.geometry("600x50")
		# self.controller.app.eval(f'tk::PlaceWindow {str(new_window)} center')

		stage = Label(new_window, text='Starting')
		stage.place(x=25, y=10)

		curr_map = Label(new_window, text='', width=580)
		curr_map.place(x=25, y=30)

		new_window.tkraise()
		new_window.update_idletasks()
		output = 'Starting'
		while not "Insert complete" in output:
			output = str(p.stdout.readline())
			print(output)
			stage.config(text='Importing new maps. Window will close automatically when import finish.')
			curr_map.config(text=output[58:-8])
			self.controller.app.update()
			
		self.is_db_loading = False
		new_window.destroy()


	def load_config(self):
		if not path.exists('./danser/settings/default.json'):
			subprocess.call("danser")

				
		with open('./danser/settings/default.json', 'r') as f:
			self.danser_config = json.load(f)

			if not self.__is_config_exist:
				self.danser_config['General']['OsuSongsDir'] = ''
				self.danser_config['General']['OsuSkinsDir'] = ''
				self.danser_config['Skin']['Cursor']['UseSkinCursor'] = True
				self.danser_config['Skin']['Cursor']['Scale'] = 0.5
				self.danser_config['Skin']['UseColorsFromSkin'] = True
				self.danser_config['Cursor']['Colors']['EnableRainbow'] = False
				self.danser_config['Cursor']['CursorRipples'] = False
				self.danser_config['Cursor']['CursorSize']  = 12
				self.danser_config['Objects']['Sliders']['Snaking']['Out'] = False
				self.danser_config['Objects']['Colors']['Color']['EnableRainbow'] = False
				self.danser_config['Objects']['Colors']['UseComboColors'] = True
				self.danser_config['Objects']['Colors']['UseSkinComboColors'] = True
				self.danser_config['Playfield']['SeizureWarning']['Enabled'] = False
				self.danser_config['Gameplay']['Boundaries']['Enabled'] = False
				self.danser_config['Playfield']['Background']['Parallax']['Amount'] = 0
				self.danser_config['Playfield']['Background']['LoadStoryboards'] = False
				self.save_config()
				self.__is_config_exist = True

	def save_config(self):
		with open('./danser/settings/default.json', 'w') as f:
			json.dump(self.danser_config, f, indent=4)