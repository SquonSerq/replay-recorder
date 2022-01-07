from tkinter import *
from tkinter import filedialog
import json
import os

def set_env() -> None:
	os.environ['danser'] = "./danser/danser.exe"
	os.environ['ffmpeg'] = "./ffmpeg/ffmpeg.exe"

def folder_dialog(root) -> None:
	if not os.path.isdir('./danser/settings'):
		os.mkdir('./danser/settings')
	with open("./danser/settings/python_config.json", "w") as f:
		folder = filedialog.askdirectory()
		f.write(json.dumps({"osu_dir": str(folder).replace('/', '\\')}))
		root.destroy()
	
def start_render(vars):
	if not os.path.isfile(vars['replay'].get()):
		return
	replay_path = vars['replay'].get()
	skin_name = vars['skin'].get()
	str_command = f'danser -quickstart -skin="{skin_name}" -replay="{replay_path}" -record'
	popen = os.popen(str_command)
	output = popen.read()
	print(output)

def choose_replay(vars):
	file = filedialog.askopenfile()
	vars['replay'].set(str(file.name.replace('/', '\\')))
	print(vars['replay'].get())

def danser_init(root):
	os.system('danser -md5 0')
	root.destroy()

def danser_init_start():
	root = Tk()
	root.geometry("600x250")
	root.eval('tk::PlaceWindow . center')
	label = Label(root, text="Wait while Danser making up DB!")
	label.pack()
	root.after(100, lambda: danser_init(root))
	root.mainloop()

def main_window():
	root = Tk()
	vars = {}
	vars["replay"] = StringVar()
	vars["skin"] = StringVar()
	vars['skin'].set("default")

	python_config = {}
	with open('./danser/settings/python_config.json', 'r') as f:
		python_config = json.load(f)


	skin_list = ['default']
	for i in os.listdir(python_config['osu_dir']+"\\Skins"):
		skin_list.append(i)
	print(skin_list)

	replay_name = Label(root, textvariable=vars["replay"])
	skin_name = OptionMenu(root, vars["skin"], *skin_list)

	choose_replay_button = Button(root, text="Choose replay", command=lambda: choose_replay(vars))
	start_render_button = Button(root, text="Start Render", command=lambda: start_render(vars))

	replay_name.pack()
	skin_name.pack()
	choose_replay_button.pack()
	start_render_button.pack()

	root.mainloop()

def main():
	set_env()
	python_config = {}
	danser_config = {}

	if not os.path.isfile("./danser/settings/python_config.json"):
		master = Tk()
		osu_dir_button = Button(master, text="Choose osu folder", command= lambda: folder_dialog(master))
		osu_dir_button.pack()
		master.mainloop()

	if not os.path.isfile('./danser/settings/default.json'):
		popen = os.popen("danser")
		output = popen.read()
		print(output)

	with open("./danser/settings/python_config.json", "r") as f:
		python_config = json.load(f)
		
	with open("./danser/settings/default.json", "r") as f:
		danser_config = json.load(f)

		danser_config['General']['OsuSongsDir'] = python_config['osu_dir'] + "\\Songs"
		danser_config['General']['OsuSkinsDir'] = python_config['osu_dir'] + "\\Skins"
		# Config Danser to render quality game-like video
		danser_config['Skin']['Cursor']['UseSkinCursor'] = True
		danser_config['Skin']['Cursor']['Scale'] = 0.5
		danser_config['Skin']['UseColorsFromSkin'] = True
		danser_config['Cursor']['Colors']['EnableRainbow'] = False
		danser_config['Cursor']['CursorRipples'] = False
		danser_config['Cursor']['CursorSize']  = 12
		danser_config['Objects']['Sliders']['Snaking']['Out'] = False
		danser_config['Objects']['Colors']['Color']['EnableRainbow'] = False
		danser_config['Objects']['Colors']['UseComboColors'] = True
		danser_config['Objects']['Colors']['UseSkinComboColors'] = True
		danser_config['Playfield']['SeizureWarning']['Enabled'] = False
		danser_config['Gameplay']['Boundaries']['Enabled'] = False

	with open('./danser/settings/default.json', 'w') as f:
		f.write(json.dumps(danser_config, indent=4))

	danser_init_start()
	main_window()

if __name__ == "__main__":
	main()