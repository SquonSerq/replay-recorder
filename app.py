import tkinter as tk
from os import environ, getcwd
from ctypes import windll

from utils.colors import *
from utils.controller import Controller
from utils.version_check import check_version


class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.overrideredirect(1)
		self.after(10, lambda: self.set_appwindow())
		self.geometry('800x600')
		self.eval('tk::PlaceWindow . center')

		# Set PATH to danser & ffmpeg
		environ['PATH'] += f';{getcwd()}\\ffmpeg;{getcwd()}\\danser'
		
		# Create top bar
		top_bar = tk.Frame(self, height=30, **frame_lg_bg_style)
		top_bar.pack(side=tk.TOP, fill=tk.X)
		self.make_draggable(top_bar)

		app_name = tk.Label(top_bar, text='Replay Recorder', **label_lg_bg_style)
		app_name.pack(side=tk.LEFT, padx=10)

		close_button = tk.Button(top_bar, text='✕', command=self.quit, **button_titlebar_style)
		close_button.pack(side=tk.RIGHT)
		minimize_button = tk.Button(top_bar, text='—',**button_titlebar_style)
		minimize_button.pack(side=tk.RIGHT)

		# Creating main frame
		container = tk.Frame(self)
		container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		controller = Controller(container, self)

	def set_appwindow(self):
		# Adds root window to task bar
		GWL_EXSTYLE=-20
		WS_EX_TOOLWINDOW=0x00000080

		hwnd = windll.user32.GetParent(self.winfo_id())
		style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
		style = style & ~WS_EX_TOOLWINDOW
		windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

		self.wm_withdraw()
		self.after(10, lambda: self.wm_deiconify())

	def make_draggable(self, object):
		object.bind("<Button-1>", self.on_drag_start)
		object.bind("<B1-Motion>", self.on_drag_motion)

	def on_drag_start(self, event):
		self._drag_start_x = event.x
		self._drag_start_y = event.y

	def on_drag_motion(self, event):
		x = self.winfo_x() - self._drag_start_x + event.x
		y = self.winfo_y() - self._drag_start_y + event.y
		self.geometry(f'+{x}+{y}')

if __name__ == "__main__":
	if not check_version():
		print("You can download new version!")
	app = App()
	app.mainloop()
