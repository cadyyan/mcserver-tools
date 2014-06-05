"""
Base utility classes and methods
"""

import json
import logging
import os.path

SETTINGS_FILE = 'mcserver.settings'
LOGGER        = None

def setup_logging(verbose):
	"""
	Setup logger. This MUST be called before using any commands
	"""

	global LOGGER

	LOGGER     = logging.getLogger('MCServer')
	log_handler = logging.StreamHandler()
	log_handler.setFormatter(
		logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
	LOGGER.addHandler(log_handler)

	if verbose:
		LOGGER.setLevel(logging.DEBUG)

	return LOGGER

def _get_settings_path(path):
	"""
	Get what the settings file path should be for the given path
	"""

	return os.path.join(path, SETTINGS_FILE)

def _validate_server_path(path):
	"""
	Validate that the given server path is valid
	"""

	if not os.path.exists(path):
		raise Exception('Path does not exist')

	if not os.path.isdir(path):
		raise Exception('Path is not a directory')

	# TODO: this really only checks for our settings file
	# TODO: might want to check for forge jar or mc jar?
	if not os.path.exists(_get_settings_path(path)):
		raise Exception('Path does not point to valid Minecraft server')

def _get_setting(settings, name, default = None):
	"""
	Get a setting by name with default value
	"""

	return settings[name] if name in settings else default

def _get_setting_jvm(settings):
	"""
	Get the JVM setting with java as a default
	"""

	return _get_setting(settings, 'java', default = 'java')

def _get_setting_max_heap(settings):
	"""
	Get the max heap setting with 1G as a default
	"""

	return _get_setting(settings, 'heap', default = '1G')

def _get_setting_max_stack(settings):
	"""
	Get the max stack setting with 1G as a default
	"""

	return _get_setting(settings, 'stack', default = '1G')

def _get_setting_perm_gen(settings):
	"""
	Get the max perm gen setting with 32m as a default
	"""

	return _get_setting(settings, 'perm_gen', default = '32m')

def _get_setting_jar(settings):
	"""
	Get the Minecraft jar to run to start the server
	"""

	return _get_setting(settings, 'jar', default = 'minecraft_server.jar')

def load_server_settings(path):
	"""
	Load the server settings from the settings file.
	"""

	settings = None
	with open(_get_settings_path(path), 'r') as settings_file:
		settings = json.load(settings_file)

	return settings