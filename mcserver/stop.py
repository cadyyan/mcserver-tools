"""
Handling for stopping the server.
"""

from mcserver import base, config, reflection

def stop_server(path):
	"""
	Stop the server if its running in daemon mode. This doesn't work in non-daemon mode
	"""

	base._validate_server_path(path)

	settings = config.CoreConfig(path)

	base.LOGGER.info('Stopping the server...')

	launcher_config = settings.get('launcher')
	if not launcher_config:
		raise base.MCServerError('No launcher configured')

	launcher_class = reflection.get_class(launcher_config['class'])
	launcher       = launcher_class(
		path,
		**launcher_config
	)

	base.LOGGER.info('Stopping the server')
	launcher.stop()

