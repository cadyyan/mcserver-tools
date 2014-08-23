"""
Server launcher base class
"""

# pylint: disable=abstract-class-not-used

import abc

class ServerLauncher(object):
	"""
	A server launcher can be used to launch the server as some sort of
	daemon like process.
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self, server):
		"""
		Instantiate a server launcher with the given config options.
		"""

		self.server = server

	@abc.abstractmethod
	def start(self, uid, gid):
		"""
		Start the server
		"""

	def stop(self):
		"""
		Stop the server
		"""

		self.server.rcon.send_command('stop')
		self.server.rcon.wait_for_close()
		self.server.rcon.disconnect()

	def restart(self, uid, gid):
		"""
		Restart the server
		"""

		self.stop()
		self.start(uid, gid)

