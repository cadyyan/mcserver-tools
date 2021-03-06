"""
Base utility classes and methods
"""

import logging
import os.path

LOGGER = None

class MCServerError(Exception):
	"""
	Generic Minecraft server error
	"""

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

def _validate_server_path(path):
	"""
	Validate that the given server path is valid
	"""

	if not os.path.exists(path):
		raise MCServerError('Path does not exist')

	if not os.path.isdir(path):
		raise MCServerError('Path is not a directory')

