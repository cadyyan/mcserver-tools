"""
A good old fashioned Unix style daemon process
"""

import daemon
import os.path
import subprocess

from mcserver import base
from mcserver.launchers import base as launcher_base

class DaemonServerLauncher(launcher_base.ServerLauncher):
	"""
	Launch the server as a daemon process
	"""

	def start(self, jvm, max_heap,
			max_stack, perm_gen, jar, extra_args,
			uid, gid):
		command = base._build_command(jvm, max_heap, max_stack, perm_gen, jar, extra_args)
		base.LOGGER.debug('Server will start with command: {0}'.format(command))

		import sys

		with daemon.DaemonContext(
			gid               = gid,
			prevent_core      = True,
			uid               = uid,
			working_directory = os.path.abspath(self.path),
		) as daemon_context:
			process = subprocess.Popen(
				command,
				shell  = True,
			)

			process.communicate()

