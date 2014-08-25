"""
Represents a server instance
"""

import datetime
import os
import os.path
import socket
import subprocess
import tarfile

from mcserver import base, config, reflection, rcon

class Server(object):
	"""
	A server object, its configs, and parts of its state and functions.
	"""

	# TODO: maybe make this take a logger as an option?
	def __init__(self, path):
		"""
		Create a server object at the given path. The server must exist at the
		given path currently. Future plans will allow for creating a new server.
		"""

		if not os.path.exists(path):
			raise IOError('Path to server does not exist')

		self.path          = path
		self.tool_config   = config.CoreConfig(path)
		self.server_config = config.MinecraftServerConfig(path)

		self._validate_launcher_config()

		self.launcher_config = self.tool_config.get('launcher', default = None)
		self.launcher_class  = reflection.get_class(self.launcher_config.get('class'))
		self.launcher        = self.launcher_class(
			self,
			**self.launcher_config
		)

		self.admin_interface_configs = self.tool_config.get('admin_notifications', [])

		self._rcon = None

	def start(self, is_daemon = None, uid = None, gid = None):
		"""
		Start the server. Optionally takes a flag for starting as a daemon
		or not as well as what user/group to run as if it is a daemon.
		"""

		if is_daemon == None:
			is_daemon = self.tool_config.get('daemon', default = False)

		if is_daemon:
			self.launcher.start(
				uid,
				gid,
			)
		else:
			cwd = os.getcwd()
			os.chdir(self.path)

			process = subprocess.Popen(self.start_command, shell = True)

			for interface in self.admin_interfaces:
				interface.server_start(self)

			process.wait()

			os.chdir(cwd)

	def stop(self):
		"""
		Stop the server.
		"""

		self.launcher.stop()

		for interface in self.admin_interfaces:
			interface.server_stop(self)

	def restart(self, is_daemon = None, uid = None, gid = None):
		"""
		Restart the server. Takes the same arguments as starting the server.
		"""

		self.stop()
		self.start(is_daemon, uid, gid)

		for interface in self.admin_interfaces:
			interface.server_restart(self)

	def backup(self):
		"""
		Create a backup of the server.
		"""

		# The server might be running. If so then we need to prevent it
		# from saving to disk before we create an archive.
		try:
			self.rcon.send_command('say BACKUP STARTING - GOING READONLY')
			self.rcon.send_command('saveoff')

			is_running = True
		except socket.error: # We're assuming the problem was with no socket open
			is_running = False

		backup_dir  = self.backup_dir
		backup_name = '{}-{}.tar.gz'.format(
			datetime.datetime.now().isoformat(),
			self.world_name,
		)

		with tarfile.open(os.path.join(backup_dir, backup_name), 'w:gz') as tar:
			tar.add(os.path.join(self.path, self.world_name))

		if is_running:
			self.rcon.send_command('saveon')
			self.rcon.send_command('say BACKUP COMPLETE')

	@property
	def jvm(self):
		"""
		Get the Java executable to launch with.
		"""

		return self.tool_config.get('java', default = 'java')

	@property
	def heap_size(self):
		"""
		Get the max heap size for the JVM to run with.
		"""

		return self.tool_config.get('heap', default = '1G')

	@property
	def stack_size(self):
		"""
		Get the max stack size for the JVM to run with.
		"""

		return self.tool_config.get('stack', default = '1G')

	@property
	def perm_gen(self):
		"""
		Get the PermGen size for the JVM to run with.
		"""

		return self.tool_config.get('perm_gen', default = '32m')

	@property
	def jar(self):
		"""
		Get the jar file to use when starting the server.
		"""

		return self.tool_config.get('jar', default = 'minecraft_server.jar')

	@property
	def extra_start_args(self):
		"""
		Get the extra arguments to pass to the server when starting.
		"""

		return self.tool_config.get('extra_start_args', default = '')

	@property
	def start_command(self):
		"""
		Get a basic command that could be used to start the server.
		"""

		return '{jvm} -Xmx{heap} -Xms{stack} -XX:MaxPermSize={perm_gen} -jar {jar} {args}'.format(
			jvm      = self.jvm,
			heap     = self.heap_size,
			stack    = self.stack_size,
			perm_gen = self.perm_gen,
			jar      = self.jar,
			args     = self.extra_start_args,
		)

	@property
	def admin_interfaces(self):
		"""
		Get collection of admin interface objects
		"""

		return [
			self._construct_admin_interface(interface)
			for interface in self.admin_interface_configs
		]

	@property
	def rcon(self):
		"""
		Get an RCon instance. This may fail if RCon is not setup on the
		server OR the server isn't running.
		"""

		if not self._rcon:
			self._rcon = rcon.RConClient(self.server_config)
			self._rcon.connect(self.server_config)

		return self._rcon

	@property
	def backup_dir(self):
		"""
		Get the directory that backups should be stored in. This will
		be created if it does not exist.
		"""

		directory = os.path.join(
			self.path,
			self.tool_config.get('backup_dir', default = 'backups'),
		)

		if not os.path.exists(directory):
			os.makedirs(directory)

		return directory

	@property
	def world_name(self):
		"""
		Get the world name.
		"""

		return self.server_config.get('level-name')

	def _construct_admin_interface(self, interface_config):
		"""
		Build an interface from the configuration
		"""

		if 'class' not in interface_config:
			raise base.MCServerError('Improperly configure admin interface')

		interface_class = reflection.get_class(interface_config['class'])

		return interface_class(**interface_config)

	def _validate_launcher_config(self):
		"""
		Try and do some basic validation on the launcher config
		"""

		if not self.tool_config.has('launcher'):
			raise base.MCServerError('No server launcher configured')

		if 'class' not in self.tool_config.get('launcher'):
			raise base.MCServerError('No launcher class configured')

