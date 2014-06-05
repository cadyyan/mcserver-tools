"""
Utlities for starting the server
"""

from __future__ import print_function

import subprocess

from mcserver import base

def start_server(path, is_daemon = False):
	"""
	Start the server. Optionally start it as a daemon.
	"""

	base._validate_server_path(path)

	settings = base.load_server_settings(path)

	jvm       = base._get_setting_jvm(settings)
	max_heap  = base._get_setting_max_heap(settings)
	max_stack = base._get_setting_max_stack(settings)
	perm_gen  = base._get_setting_perm_gen(settings)
	jar       = base._get_setting_jar(settings)

	command = '{jvm} -Xmx={heap} -Xms={stack} -XX:MaxPermSize={perm_gen} -jar {jar}'.format(
		jvm = jvm, heap = max_heap, stack = max_stack, perm_gen = perm_gen, jar = jar)

	base.LOGGER.info('Starting server...')
	base.LOGGER.debug('Starting server with `{0}`'.format(command))

	process = subprocess.Popen(command, shell = True)

	if is_daemon:
		base.LOGGER.warn('Daemon not supported yet, falling back to non-daemon')
		process.wait()
	else:
		process.wait()
