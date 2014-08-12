"""
TMUX terminal interface
"""

from mcserver import base
from mcserver.base import MCServerError
from mcserver.launchers import base as launcher_base

import os.path
import subprocess
import tmuxp

class TmuxServerLauncher(launcher_base.ServerLauncher):
	"""
	TMUX based launcher
	"""

	def __init__(self, path, *args, **kwargs):
		"""
		Create a new TMUX terminal interface.
		"""

		super(TmuxServerLauncher, self).__init__(
			path,
			*args,
			**kwargs
		)

		self._validate_config(*args, **kwargs)

		self.session_name = kwargs['session']
		self.window_name  = kwargs['window']

		self.server  = tmuxp.Server()
		self.session = self._get_session()
		self.window  = self._get_window()
		self.pane    = self._get_pane()

	def start(self, jvm, max_heap,
			max_stack, perm_gen, jar, extra_args,
			uid, gid):
		command = base._build_command(jvm, max_heap, max_stack, perm_gen, jar, extra_args)

		base.LOGGER.debug('Server will start with command: {0}'.format(command))
		self.pane.send_keys(command)

		subprocess.check_output(
			'echo $! > {0}'.format(
				base._get_pidfile(self.path),
			),
			shell = True,
		) # TODO: not at all cross platform :-/

	def _validate_config(*args, **kwargs):
		"""
		Validate config settings.
		"""

		if 'session' not in kwargs:
			raise MCServerError('No session name given for TMUX interface')

		if 'window' not in kwargs:
			raise MCServerError('No window name given for TMUX interface')

	def _get_session(self):
		"""
		Get or create the session.
		"""

		if self.server.has_session(self.session_name):
			return self.server.findWhere({'session_name': self.session_name})

		return self.server.new_session(session_name    = self.session_name)

	def _get_window(self):
		"""
		Get or create the window.
		"""

		window = self.session.findWhere({'window_name': self.window_name})
		if window:
			return window

		return self.session.new_window(
			start_directory = os.path.abspath(self.path),
			window_name     = self.window_name,
		)

	def _get_pane(self):
		"""
		Get or create the pane.
		"""

		# We always assume that the first pane is the correct one *gulp*
		return self.window.select_pane(0)
