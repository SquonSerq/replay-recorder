import tkinter as tk
from ctypes import windll

from utils.colors import *


class DraggableWindow():
	def __init__(self, parent, width, height, frame_name=''):
		self.parent = parent
		self.parent.title(frame_name)
		self.parent.configure(**frame_border)
		self.parent.overrideredirect(True)
		self.set_appwindow()
		self.set_geometry(width, height)

		top_bar = tk.Frame(parent, height=30, **frame_lg_bg_style)
		top_bar.pack(side=tk.TOP, fill=tk.X)
		top_bar.pack_propagate(0)
		top_bar.bind("<Button-1>", self.on_drag_start)
		top_bar.bind("<B1-Motion>", self.on_drag_motion)
		frame_name = tk.Label(top_bar, text=frame_name, **label_lg_style)
		frame_name.pack(side=tk.LEFT, padx=10)
		close_button = tk.Button(top_bar, text='✕', command=parent.destroy, **button_titlebar_style)
		close_button.pack(side=tk.RIGHT)

	def set_appwindow(self):
		self.parent.update()

		# Adds root window to task bar
		GWL_EXSTYLE=-20
		WS_EX_APPWINDOW=0x00040000
		WS_EX_TOOLWINDOW=0x00000080
		self.parent.update()
		hwnd = windll.user32.GetParent(self.parent.winfo_id())
		style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
		style = style & ~WS_EX_TOOLWINDOW
		style = style | WS_EX_APPWINDOW
		windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

		self.parent.wm_withdraw()
		self.parent.wm_deiconify()

	def on_drag_start(self, event):
		self.parent._drag_start_x = event.x
		self.parent._drag_start_y = event.y

	def on_drag_motion(self, event):
		x = self.parent.winfo_x() - self.parent._drag_start_x + event.x
		y = self.parent.winfo_y() - self.parent._drag_start_y + event.y
		self.parent.geometry(f'+{x}+{y}')

	def set_geometry(self, width, height):
		x_pos = int(self.parent.winfo_screenwidth()/2 - width/2)
		y_pos = int(self.parent.winfo_screenheight()/2 - height/2)
		self.parent.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
