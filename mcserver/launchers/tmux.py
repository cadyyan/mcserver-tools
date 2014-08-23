"""
TMUX terminal interface
"""

from mcserver.base      import MCServerError
from mcserver.launchers import base as launcher_base

import os
import os.path
import tmuxp

class TmuxServerLauncher(launcher_base.ServerLauncher):
	"""
	TMUX based launcher
	"""

	def __init__(self, server, *args, **kwargs):
		"""
		Create a new TMUX terminal interface.
		"""

		super(TmuxServerLauncher, self).__init__(server)

		self._validate_config(*args, **kwargs)

		self.session_name = kwargs['session']
		self.window_name  = kwargs['window']

		self._tmux_server = None
		self._session     = None
		self._window      = None
		self._pane        = None

	def start(self, uid, gid):
		if uid:
			os.setuid(uid)

		if gid:
			os.setgid(gid)

		self.pane.send_keys(self.server.start_command)

	def _validate_config(self, *args, **kwargs):
		"""
		Validate config settings.
		"""

		if 'session' not in kwargs:
			raise MCServerError('No session name given for TMUX interface')

		if 'window' not in kwargs:
			raise MCServerError('No window name given for TMUX interface')

	@property
	def tmux_server(self):
		"""
		tmux server
		"""

		if not self._tmux_server:
			self._tmux_server = tmuxp.Server()

		return self._tmux_server

	@property
	def session(self):
		"""
		tmux session
		"""

		if not self._session:
			self._session = self._get_session()

		return self._session

	@property
	def window(self):
		"""
		tmux window
		"""

		if not self._window:
			self._window = self._get_window()

		return self._window

	@property
	def pane(self):
		"""
		tmux pane
		"""

		if not self._pane:
			self._pane = self._get_pane()

		return self._pane

	def _get_session(self):
		"""
		Get or create the session.
		"""

		if self.tmux_server.has_session(self.session_name):
			return self.tmux_server.findWhere({'session_name': self.session_name})

		return self.tmux_server.new_session(session_name    = self.session_name)

	def _get_window(self):
		"""
		Get or create the window.
		"""

		window = self.session.findWhere({'window_name': self.window_name})
		if window:
			return window

		return self.session.new_window(
			start_directory = os.path.abspath(self.server.path),
			window_name     = self.window_name,
		)

	def _get_pane(self):
		"""
		Get or create the pane.
		"""

		# We always assume that the first pane is the correct one *gulp*
		return self.window.select_pane(0)

