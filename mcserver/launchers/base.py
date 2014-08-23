"""
Server launcher base class
"""

import abc

from mcserver import config, rcon

class ServerLauncher(object):
	"""
	A server launcher can be used to launch the server as some sort of
	daemon like process.
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self, path):
		"""
		Instantiate a server launcher with the given config options.
		"""

		self.path              = path
		self.server_properties = config.MinecraftServerConfig(path)
		self.rcon              = rcon.RConClient(self.server_properties)

	@abc.abstractmethod
	def start(self, server, uid, gid):
		"""
		Start the server
		"""

	def stop(self):
		"""
		Stop the server
		"""

		self.rcon.connect(self.server_properties)
		self.rcon.send_command('stop')
		self.rcon.wait_for_close()
		self.rcon.disconnect()

	def restart(self, server, uid, gid):
		"""
		Restart the server
		"""

		self.rcon.connect(self.server_properties)
		self.stop()
		self.start(server, uid, gid)

