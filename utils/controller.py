from models.config import Config
from pages.main_menu import MainMenu
from pages.pre_settings import PreSettings
from pages.settings import Settings

class Controller():
	def __init__(self, container):

		self.config = Config()
		self.config.load_config()

		# Create frames for other menus. This allows us to switch between them
		self.frames = {}
		for F in (MainMenu, PreSettings, Settings):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky='nsew')

		if self.config.is_dirs_valid():
			self.show_frame('MainMenu')
		else:
			self.show_frame('PreSettings')

	def show_frame(self, page_name):
		'''Shows frame by its name'''
		frame = self.frames[page_name]
		frame.tkraise()
