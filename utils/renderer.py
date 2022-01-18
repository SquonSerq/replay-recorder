import subprocess
import threading
import queue
import re


class Renderer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.is_running = True
		self.selected_replays = []
		self.queue = queue.Queue()

	def run(self):
		while self.is_running:
			replay_data = self.queue.get()
			if not replay_data:
				continue
			
			p = subprocess.Popen(f'danser -quickstart \
				-skin="{replay_data["selected_skin"]}" \
				-replay="{replay_data["replay_path"]}" \
				-record', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
			
			for line in iter(p.stdout.readline,''):
				line = str(line.rstrip())
				print(line)
				if not p.poll() is None:
					break
				
				if 'Progress:' in line:
					replay_data['frame'].children['!progressbar']['value'] = int(re.search("Progress: ([0-9]*)%", line).group(1))
			self.queue.task_done()

	def add_replay_to_render(self, frame, replay_path, selected_skin):
		self.selected_replays.append({
			'frame': frame,
			'replay_path': replay_path,
			'selected_skin': selected_skin
		})

	def render_video(self):
		if not self.selected_replays:
			print('No replays')
			return

		for replay_data in self.selected_replays:
			self.queue.put_nowait(replay_data)

		self.selected_replays = []
