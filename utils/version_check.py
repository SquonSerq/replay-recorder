import requests

def check_version():
	try:
		r = requests.get("https://raw.githubusercontent.com/SquonSerq/replay-recorder/main/version", timeout=2).text
	except requests.exceptions.Timeout:
		return True

	ver = ''
	with open("version", 'r') as f:
		ver = str(f.read())

	if r == ver:
		return True
	return False


	