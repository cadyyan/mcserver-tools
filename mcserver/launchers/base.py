"""
Server launcher base class
"""

import abc
import os.path
import re

from mcserver import base, rcon

class ServerLauncher(object):
	"""
	A server launcher can be used to launch the server as some sort of
	daemon like process.
	"""

	SERVER_PROPERTY_REGEX = re.compile(r'^\s*(?P<property>[^\s=#]+)=(?P<value>[^#\n\r]+)*\s*$')

	__metaclass__ = abc.ABCMeta

	def __init__(self, path, *args, **kwargs):
		"""
		Instantiate a server launcher with the given config options.
		"""

		self.path              = path
		self.server_properties = self._load_server_properties()
		self.rcon              = rcon.RConClient(self.server_properties)

	@abc.abstractmethod
	def start(self, jvm, max_heap,
			  max_stack, perm_gen, jar, extra_args,
			  uid, gid):
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

	def restart(self, jvm, max_heap,
				max_stack, perm_gen, jar, extra_args,
				uid, gid):
		"""
		Restart the server
		"""

		self.rcon.connect(self.server_properties)
		self.stop()
		self.start(jvm, max_heap, max_stack, perm_gen, jar, extra_args, uid, gid)

	def _load_server_properties(self):
		"""
		Attempt to load the server properties. If the properties file does not
		exist them for now we'll just give an empty set of properties. Might
		generate a default one eventually ;)
		"""

		server_properties = {}

		base.LOGGER.info('Loading server properties...')

		properties_file = os.path.join(self.path, 'server.properties')
		if not os.path.exists(properties_file):
			base.LOGGER.info('Server properties file does not exist. Skipping')
			return

		with open(properties_file, 'r') as fh:
			lines = fh.readlines()

			for line in lines:
				line = line.strip()
				base.LOGGER.debug(line)

				m = self.SERVER_PROPERTY_REGEX.match(line)
				if not m:
					continue

				(prop, value) = m.groups()
				base.LOGGER.debug('Found property/value: {0}:{1}'.format(prop, value))

				server_properties[prop] = value

		return server_properties
