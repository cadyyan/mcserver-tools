"""
RCon client for Minecraft
"""

import re
import select
import socket
import struct

from mcserver import base

class RConClient(object):
	"""
	Remote console client for Minecraft (only connects to localhost)
	"""

	COMMAND_TYPE = 2
	ERROR_REGEX  = re.compile(r'^Error executing: [^\(]* \((?P<response>.*)\)$')
	LOGIN_ERROR  = -1
	LOGIN_TYPE   = 3
	TERMINATOR   = '\x00\x00'

	def __init__(self, server_settings):
		"""
		Set up client but do not connect
		"""

		if not server_settings['enable-rcon']:
			raise Exception('RCon not enabled on server')

		self.host   = '127.0.0.1'
		self.port   = server_settings.get('rcon.port') or 25575
		self.socket = self._create_socket()

	def connect(self, server_settings):
		"""
		Connect to the RCon server
		"""

		base.LOGGER.debug('Connecting to RCon on port {}'.format(self.port))

		if 'rcon.password' not in server_settings:
			raise IOError('No RCon password specified')

		self.socket.connect((self.host, int(self.port)))
		self._send_raw(self.LOGIN_TYPE, server_settings.get('rcon.password'))

	def disconnect(self):
		"""
		Disconnect from the RCon server
		"""

		self.socket.close()

		self.socket = self._create_socket()

	def _send_raw(self, data_type, data):
		"""
		Send raw data to the server
		"""

		send_buffer = struct.pack(
			'<iii',
			10 + len(data),
			0,
			data_type
		) + data + self.TERMINATOR

		self.socket.send(send_buffer)

		response = ''
		ready    = True
		while ready:
			length, req_id, resp_type = struct.unpack('<iii', self.socket.recv(12))
			resp_data                 = self.socket.recv(length - 8)

			if resp_data[-2:] != self.TERMINATOR:
				raise IOError('Protocol error: missing null padding')

			data = data[:-2]

			if req_id == self.LOGIN_ERROR:
				raise IOError('Invalid login')

			match = self.ERROR_REGEX.match(resp_data)
			if match:
				raise Exception('Command failed: ' + match.group('response'))

			response += resp_data
			ready     = select.select([self.socket], [], [], 0)[0]

		response.replace(self.TERMINATOR, '')

		return response

	def send_command(self, command):
		"""
		Send command to server
		"""

		return self._send_raw(self.COMMAND_TYPE, command)

	def wait_for_close(self):
		"""
		Wait for the socket to get closed
		"""

		self.socket.settimeout(30)
		self.socket.recv(12)

	def _create_socket(self):
		"""
		Create a new socket
		"""

		return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
