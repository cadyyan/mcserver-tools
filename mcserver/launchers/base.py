"""
Server launcher base class
"""

import abc

from mcserver import base

class ServerLauncher(object):
	"""
	A server launcher can be used to launch the server as some sort of
	daemon like process.
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self, path, jvm, max_heap,
				 max_stack, perm_gen, jar, extra_args,
				 uid, gid,
				 *args, **kwargs):
		"""
		Instantiate a server launcher with the given config options.
		"""

		self.path       = path
		self.jvm        = jvm
		self.max_heap   = max_heap
		self.max_stack  = max_stack
		self.perm_gen   = perm_gen
		self.jar        = jar
		self.extra_args = extra_args
		self.uid        = uid
		self.gid        = gid
		self.command    = self._build_command()

		base.LOGGER.debug('Server will start with command: {0}'.format(self.command))

	@abc.abstractmethod
	def start(self):
		"""
		Start the server
		"""

	@abc.abstractmethod
	def stop(self):
		"""
		Stop the server
		"""

	def restart(self):
		"""
		Restart the server
		"""

		stop()
		start()

	def _build_command(self):
		"""
		Build the command for starting the server
		"""

		return '{jvm} -Xmx{heap} -Xms{stack} -XX:MaxPermSize={perm_gen} -jar {jar} {args}'.format(
			jvm      = self.jvm,
			heap     = self.max_heap,
			stack    = self.max_stack,
			perm_gen = self.perm_gen,
			jar      = self.jar,
			args     = self.extra_args,
		)
