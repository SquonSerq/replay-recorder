def enqueue_output(out, q):
	for line in iter(out.readline, b''):
		q.put(line)
	out.close()