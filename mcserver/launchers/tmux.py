"""
TMUX terminal interface
"""

from mcserver import base
from mcserver.base import MCServerError
from mcserver.launchers import base as launcher_base

import os
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

		self._server  = None
		self._session = None
		self._window  = None
		self._pane    = None

	def start(self, jvm, max_heap,
			max_stack, perm_gen, jar, extra_args,
			uid, gid):

		if uid:
			os.setuid(uid)

		if gid:
			os.setgid(gid)

		command = base._build_command(jvm, max_heap, max_stack, perm_gen, jar, extra_args)

		self.pane.send_keys(command)

	def _validate_config(self, *args, **kwargs):
		"""
		Validate config settings.
		"""

		if 'session' not in kwargs:
			raise MCServerError('No session name given for TMUX interface')

		if 'window' not in kwargs:
			raise MCServerError('No window name given for TMUX interface')

	@property
	def server(self):
		"""
		tmux server
		"""

		if self._server:
			return self._server

		self._server = tmuxp.Server()
		return self._server

	@property
	def session(self):
		"""
		tmux session
		"""

		if self._session:
			return self._session

		self._session = self._get_session()
		return self._session

	@property
	def window(self):
		"""
		tmux window
		"""

		if self._window:
			return self._window

		self._window = self._get_window()
		return self._window

	@property
	def pane(self):
		"""
		tmux pane
		"""

		if self._pane:
			return self._pane

		self._pane = self._get_pane()
		return self._pane

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
