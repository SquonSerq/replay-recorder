import subprocess
import threading
import queue
import re


class Renderer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.is_running = True
		self.render_queue = queue.Queue()

	def run(self):
		while self.is_running:
			replay_data = self.render_queue.get()
			
			p = subprocess.Popen(f'danser -quickstart \
				-skin="{replay_data[2]}" \
				-replay="{replay_data[1]}" \
				-record', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
			
			for line in iter(p.stdout.readline,''):
				line = str(line.rstrip())
				print(line)
				if not p.poll() is None:
					break
				
				if 'Progress:' in line:
					replay_data[0].children['!progressbar']['value'] = int(re.search("Progress: ([0-9]*)%", line).group(1))
			self.render_queue.task_done()

	def add_replay_to_queue(self, replay_data):
		self.render_queue.put_nowait(replay_data)
