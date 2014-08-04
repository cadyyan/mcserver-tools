"""
Server launcher base class
"""

import abc

class ServerLauncher(object):
	"""
	A server launcher can be used to launch the server as some sort of
	daemon like process.
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self, path, *args, **kwargs):
		"""
		Instantiate a server launcher with the given config options.
		"""

		self.path = path

	@abc.abstractmethod
	def start(self, jvm, max_heap,
			  max_stack, perm_gen, jar, extra_args,
			  uid, gid):
		"""
		Start the server
		"""

	@abc.abstractmethod
	def stop(self):
		"""
		Stop the server
		"""

	def restart(self, jvm, max_heap,
				max_stack, perm_gen, jar, extra_args,
				uid, gid):
		"""
		Restart the server
		"""

		stop()
		start(jvm, max_heap, max_stack, perm_gen, jar, extra_args, uid, gid)

	def _build_command(self, jvm, max_heap,
					   max_stack, perm_gen, jar, extra_args):
		"""
		Build the command for starting the server
		"""

		return '{jvm} -Xmx{heap} -Xms{stack} -XX:MaxPermSize={perm_gen} -jar {jar} {args}'.format(
			jvm      = jvm,
			heap     = max_heap,
			stack    = max_stack,
			perm_gen = perm_gen,
			jar      = jar,
			args     = extra_args,
		)
