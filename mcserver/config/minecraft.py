"""
Reads the Minecraft server properties file
"""

import os.path
import re

class MinecraftServerConfig(object):
	"""
	Minecraft server configuration
	"""

	PROPERTY_REGEX = re.compile(r'^\s*(?P<property>[^\s=#]+)=(?P<value>[^#\n\r]+)*\s*$')
	SETTINGS_FILE  = 'server.properties'

	def __init__(self, path):
		"""
		Load the server configuration from the given server directory. Path is
		the directory of the server.
		"""

		self.settings_file = os.path.join(path, self.SETTINGS_FILE)
		self._settings     = {}

		self._load_settings()

	def _load_settings(self):
		"""
		Load the settings from disk.
		"""

		self._settings = {}

		with open(self.settings_file, 'r') as fh:
			for line in fh.readlines():
				line = line.strip()

				m = self.PROPERTY_REGEX.match(line)
				if not m:
					continue

				(prop, value) = m.groups()

				self._settings[prop] = value

	def get(self, property, default = None):
		"""
		Try to get the property value. If the property value was not found
		then return the given default. If the value is found it will be
		returned as a string.
		"""

		if property not in self._settings:
			return default

		return self._settings[property]

	def get_int(self, property, default = None):
		"""
		Try to get the property value as an integer. If the property was
		not found then return the given default. If the value is found
		then try to coerce it into an integer.
		"""

		ret = self.get(property, default)

		if ret:
			ret = int(ret)

		return ret

	def get_float(self, property, default = None):
		"""
		Try to get the property value as a float. If the property was
		not found tehn return the given default. If the value is found
		then try to coerce it into a float.
		"""

		ret = self.get(property, default)

		if ret:
			ret = float(ret)

		return ret

