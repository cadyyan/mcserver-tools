import base
from mcserver import config

import os.path
import pybullet

class PushBulletNotification(base.AdminNotificationInterface):
	"""
	Notifications via PushBullet
	"""

	def __init__(self, **kwargs):
		super(PushBulletNotification, self).__init__(**kwargs)

		self._validate_config(**kwargs)

		self.access_token  = kwargs['access_token']
		self.auth_type     = kwargs['auth_type']
		self.client_id     = kwargs['client_id'] if 'client_id' in kwargs else None
		self.client_secret = kwargs['client_secret'] if 'client_secret' in kwargs else None
		self.config        = {
			'auth': {
				'access_token':  self.access_token,
				'type':     self.auth_type,
				'client_id':     self.client_id,
				'client_secret': self.client_secret,
			}
		}

		self.client = pybullet.Client(self.config)

	def server_start(self, server):
		self.client.push(
			'note',
			title = 'Server Started',
			body  = 'Minecraft server ({}) was started'.format(
				self._get_server_name(server),
			),
		)

	def server_stop(self, server):
		self.client.push(
			'note',
			title = 'Server Stopped',
			body  = 'Minecraft server ({}) was stopped'.format(
				self._get_server_name(server),
			),
		)

	def server_restart(self, server):
		self.client.push(
			'note',
			title = 'Server Restarted',
			body  = 'Minecraft server ({}) was restarted'.format(
				self._get_server_name(server),
			),
		)

	def _get_server_name(self, server):
		"""
		Attempt to get the server name
		"""

		return os.path.basename(os.path.abspath(server.path))

	def _validate_config(self, **kwargs):
		"""
		Validate the config options that are required
		"""

		if 'auth_type' not in kwargs:
			raise config.ConfigurationException('Authentiation type required for PushBullet')

		if 'access_token' not in kwargs:
			raise config.ConfigurationException('Access token required for PushBullet')

		auth_type = kwargs['auth_type']

		if auth_type == 'oauth':
			if 'client_id' not in kwargs:
				raise config.ConfigurationException('Client ID is required for PushBullet')

			if 'client_secret' not in kwargs:
				raise config.ConfigurationException('Client secret is required for PushBullet')

