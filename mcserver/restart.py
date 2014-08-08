"""
Handle restarts
"""

from mcserver import start, stop

def restart_server(path, is_daemon = False, uid = None, gid = None):
	"""
	Handle server restarts
	"""

	stop.stop_server(path)
	start.start_server(path, is_daemon = is_daemon, uid = uid, gid = gid)
