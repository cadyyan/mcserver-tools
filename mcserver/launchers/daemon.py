"""
A good old fashioned Unix style daemon process
"""

import daemon
import lockfile.pidlockfile
import os.path
import subprocess

from mcserver import base
from mcserver.launchers import base as launcher_base

class DaemonServerLauncher(launcher_base.ServerLauncher):
	"""
	Launch the server as a daemon process

	TODO: deprecated for now till interfaces are a thing :-/
	"""

	def start(self):
		pidfile = os.path.abspath(base._get_pidfile(path))
		if not os.path.exists(pidfile):
			open(pidfile, 'w').close() # touch pidfile

		with daemon.DaemonContext(
			gid               = gid,
			pidfile           = lockfile.pidlockfile.PIDLockFile(pidfile),
			prevent_core      = True,
			uid               = uid,
			working_directory = path,
		) as daemon_context:
			process = subprocess.Popen(
				self.command,
				shell  = True,
				# TODO: need to register something to stdout/stderr
			)

			process.communicate()

	def stop(self):
		pass # TODO:
