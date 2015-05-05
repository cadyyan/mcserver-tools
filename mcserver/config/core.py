"""
MCServer Tools config loader
"""

import json
import os.path

from mcserver import MCServerError

class CoreConfig(object):
	"""
	MCServer Tools configuration
	"""

	SETTINGS_FILE = 'mcserver.settings'

	def __init__(self, path):
		"""
		Load configuration from the given file path
		"""

		self.settings_file = os.path.join(path, self.SETTINGS_FILE)
		self._settings     = {}

		self._load_settings()

	def _load_settings(self):
		"""
		Load the settings from disk
		"""

		try:
			with open(self.settings_file, 'r') as fh:
				self._settings = json.load(fh)
		except:
			raise MCServerError('Could not open settings file: {}'.format(self.settings_file))

	def get(self, property, default = None):
		"""
		Try to get the property value. If the property was not found
		then return the given default.
		"""

		if property not in self._settings:
			return default

		return self._settings[property]

	def has(self, property):
		"""
		Check if the config has the given property.
		"""

		return property in self._settings

