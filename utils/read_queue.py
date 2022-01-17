import subprocess
import threading
import re

class Render(threading.Thread):
	def __init__(self, queue, output):
		threading.Thread.__init__(self)
		self.is_running = True
		self.queue = queue
		self.output = output

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

def enqueue_output(out, q):
	for line in iter(out.readline, b''):
		q.put(line)
	out.close()
