"""
Represents a server instance
"""

import os
import os.path
import subprocess

from mcserver import base, config, reflection

class Server(object):
	"""
	A server object, its configs, and parts of its state and functions.
	"""

	# TODO: maybe make this take a logger as an option?
	def __init__(self, path):
		"""
		Create a server object at the given path. The server must exist at the
		given path currently. Future plans will allow for creating a new server.
		"""

		if not os.path.exists(path):
			raise IOError('Path to server does not exist')

		self.path          = path
		self.tool_config   = config.CoreConfig(path)
		self.server_config = config.MinecraftServerConfig(path)

	def start(self, is_daemon = None, uid = None, gid = None):
		"""
		Start the server. Optionally takes a flag for starting as a daemon
		or not as well as what user/group to run as if it is a daemon.
		"""

		jvm        = self.tool_config.get('java',             default = 'java')
		max_heap   = self.tool_config.get('heap',             default = '1G')
		max_stack  = self.tool_config.get('stack',            default = '1G')
		perm_gen   = self.tool_config.get('perm_gen',         default = '32m')
		jar        = self.tool_config.get('jar',              default = 'minecraft_server.jar')
		extra_args = self.tool_config.get('extra_start_args', default = '')

		if is_daemon == None:
			is_daemon = self.tool_config.get('daemon', default = False)

		if is_daemon:
			launcher_config = self.tool_config.get('launcher')
			if not launcher_config:
				raise base.MCServerError('No server launcher configured')

			launcher_class = reflection.get_class(launcher_config['class'])

			launcher = launcher_class(
				self.path,
				**launcher_config
			)

			launcher.start(
				jvm,
				max_heap,
				max_stack,
				perm_gen,
				jar,
				extra_args,
				uid,
				gid,
			)
		else:
			cwd = os.getcwd()
			os.chdir(self.path)

			command = base._build_command(jvm, max_heap, max_stack, perm_gen, jar, extra_args)
			process =  subprocess.Popen(command, shell = True)

			process.wait()

			os.chdir(cwd)

	def stop(self):
		"""
		Stop the server.
		"""

		launcher_config = self.tool_config.get('launcher')
		if not launcher_config:
			raise base.MCServerError('No server launcher configured')

		launcher_class = reflection.get_class(launcher_config['class'])
		launcher       = launcher_class(
			self.path,
			**launcher_config
		)

		launcher.stop()

	def restart(self, is_daemon = None, uid = None, gid = None):
		"""
		Restart the server. Takes the same arguments as starting the server.
		"""

		self.stop()
		self.start(is_daemon, uid, gid)

