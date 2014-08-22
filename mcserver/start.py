"""
Utlities for starting the server
"""

import os
import os.path
import subprocess

from mcserver import base, config, reflection

def start_server(path, is_daemon = None, uid = None, gid = None):
	"""
	Start the server. Optionally start it as a daemon.
	"""

	base._validate_server_path(path)

	settings = config.CoreConfig(path)

	jvm        = settings.get('java',             default = 'java')
	max_heap   = settings.get('heap',             default = '1G')
	max_stack  = settings.get('stack',            default = '1G')
	perm_gen   = settings.get('perm_gen',         default = '32m')
	jar        = settings.get('jar',              default = 'minecraft_server.jar')
	extra_args = settings.get('extra_start_args', default = '')

	base.LOGGER.info('Starting server...')

	if is_daemon == None:
		is_daemon = settings.get('daemon', default = False)

	if not is_daemon:
		if uid != None:
			base.LOGGER.warn('User option is ignored when not running as a daemon')
			uid = None
		if gid != None:
			base.LOGGER.warn('Group option is ignored when not running as a daemon')
			gid = None

	if is_daemon:
		base.LOGGER.debug(
			'Starting daemon process with user and group: {user}, {group}'.format(
				user  = uid,
				group = gid,
			)
		)

		launcher_config = settings.get('launcher')
		if not launcher_config:
			raise base.MCServerError('No server launcher configured')

		launcher_class = reflection.get_class(launcher_config['class'])

		launcher = launcher_class(
			path,
			**launcher_config
		)
		launcher.start(
			jvm,
			max_heap,
			max_stack,
			perm_gen,
			jar,
			extra_args,
			uid,
			gid,
		)
	else:
		cwd = os.getcwd()
		os.chdir(os.path.join(path))

		command = base._build_command(jvm, max_heap, max_stack, perm_gen, jar, extra_args)
		base.LOGGER.debug('Starting server with command {0}'.format(command))

		process = subprocess.Popen(command, shell = True) # TODO: theres no more command here!

		process.wait()

		os.chdir(cwd)

