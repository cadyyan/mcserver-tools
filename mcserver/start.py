"""
Utlities for starting the server
"""

import daemon
import lockfile.pidlockfile
import os
import os.path
import subprocess

from mcserver import base, reflection

def start_server(path, is_daemon = False, uid = None, gid = None):
	"""
	Start the server. Optionally start it as a daemon.
	"""

	base._validate_server_path(path)

	settings = base.load_server_settings(path)

	jvm        = base._get_setting_jvm(settings)
	max_heap   = base._get_setting_max_heap(settings)
	max_stack  = base._get_setting_max_stack(settings)
	perm_gen   = base._get_setting_perm_gen(settings)
	jar        = base._get_setting_jar(settings)
	extra_args = base._get_extra_start_args(settings)

	base.LOGGER.info('Starting server...')

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

		launcher_config = base._get_launcher(settings)
		launcher_class  = reflection.get_class(launcher_config['class'])

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
		command = base._build_command(jvm, max_heap, max_stack, perm_gen, jar, extra_args)
		base.LOGGER.debug('Starting server with command {0}'.format(command))

		process = subprocess.Popen(command, shell = True) # TODO: theres no more command here!

		process.wait()
