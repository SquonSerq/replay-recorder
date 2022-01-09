from tkinter import StringVar
from json import load, dump
from subprocess import Popen
from os import path

class Config:
	def __init__(self):
		self.replay_path = ''
		self.skin_name = StringVar()
		self.danser_config = {}

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

	def load_config(self):
		if not path.exists('./danser/settings/default.json'):
			Popen('danser')
		with open('./danser/settings/default.json', 'r') as f:
			self.danser_config = load(f)

	def save_config(self):
		with open('./danser/settings/default.json', 'w') as f:
			dump(self.danser_config, f)