import requests

def check_version():
	ver = ''
	with open("version", 'r') as f:
		ver = str(f.read())

	r = requests.get("https://raw.githubusercontent.com/SquonSerq/replay-recorder/main/version").text

	if r == ver:
		return True
	return False


	