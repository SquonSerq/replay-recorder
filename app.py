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

		# Установка окружения для ffmpeg и danser
		environ['PATH'] += f';{getcwd()}/ffmpeg;{getcwd()}/danser'

		# Подгрузка конфига
		if not path.exists('./danser/settings/default.json'):
			Popen('danser')
		with open('./danser/settings/default.json', 'r') as f:
			self.config = load(f)

		# Создание основного фрейма для главного окна
		container = Frame(self)
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# Создадим фреймы для остальных окон, чтобы между ними можно было переключаться
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
					print('Указан неверный путь до папки с песнями')
					return False
			else:
				print('Не указан путь до папки с песнями')
				return False

			if self.config['General']['OsuSkinsDir']:
				if not path.exists(self.config['General']['OsuSkinsDir']):
					print('Указан неверный путь до папки со скинами')
					return False
			else:
				print('Не указан путь до папки со скинами')
				return False
			return True 

	def save_config(self):
		with open('./danser/settings/default.json', 'w') as f:
			dump(self.config, f)

	def show_frame(self, page_name):
		'''Показывает фрейм по его имени'''
		frame = self.frames[page_name]
		frame.tkraise()

app = App()
app.mainloop()
