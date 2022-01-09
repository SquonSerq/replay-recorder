from tkinter import Button, END, Entry, filedialog, Frame, Label


class PreSettings(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		
		def choose_songs_dir():
			directory = filedialog.askdirectory()
			if directory:
				songs_folder.config(state='normal')
				self.controller.config.danser_config['General']['OsuSongsDir'] = directory
				songs_folder.delete(0, END)
				songs_folder.insert(END, self.controller.config.danser_config['General']['OsuSongsDir'])
				songs_folder.config(state='readonly')
		
		def choose_skins_dir():
			directory = filedialog.askdirectory()
			if directory:
				skin_folder.config(state='normal')
				self.controller.config.danser_config['General']['OsuSkinsDir'] = directory
				skin_folder.delete(0, END)
				skin_folder.insert(END, self.controller.config.danser_config['General']['OsuSkinsDir'])
				skin_folder.config(state='readonly')

		def go_main_menu():
			# If everything is alright, write and get back to main menu
			if self.controller.config.is_dirs_valid():
				self.controller.config.save_config()
				controller.show_frame('MainMenu')

		# If paths to songs or skins are not set or set incorrect
		# Interface to choose songs folder
		Label(self, text='OSU! Songs folder', width=20).grid(row=0, column=0)
		songs_folder = Entry(self, width=50)
		songs_folder.insert(END, self.controller.config.danser_config['General']['OsuSongsDir'])
		songs_folder.config(state='readonly')
		songs_folder.grid(row=0, column=1)
		Button(self, text='Choose', command=lambda: choose_songs_dir(), width=20).grid(row=0, column=2)

		# Interface to choose skins folder
		Label(self, text='OSU! Skins folder', width=20).grid(row=1, column=0)
		skin_folder = Entry(self, width=50)
		skin_folder.insert(END, self.controller.config.danser_config['General']['OsuSkinsDir'])
		skin_folder.config(state='readonly')
		skin_folder.grid(row=1, column=1)
		Button(self, text='Choose', command=lambda: choose_skins_dir(), width=20).grid(row=1, column=2)
		Button(self, text='Continue', command=lambda: go_main_menu(), width=20).grid(row=2, column=0, columnspan=3)
