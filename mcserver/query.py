import socket
import struct

class QueryClient(object):
	"""
	A client for connecting to a server's Query system (if its enabled).

	Heavily based upon Dinnerbone's Query implementation:
	https://github.com/Dinnerbone/mcstatus
	"""

	DEFAULT_PORT          = 25565
	MAGIC_PREFIX          = '\xFE\xFD'
	PACKET_TYPE_CHALLENGE = 9
	PACKET_TYPE_QUERY     = 0

	def __init__(self, server_settings, id = 0, retries = 2, timeout = 10):
		"""
		Set up the client. id is an identifier that can be used to know who
		requests are for. retries is the number of attempts to make before failing.
		"""

		if not server_settings.get_boolean('enable-query'):
			raise Exception('Query not enabled on server')

		self.host             = '127.0.0.1'
		self.port             = server_settings.get_int('query.port', QueryClient.DEFAULT_PORT)
		self.address          = (self.host, self.port)
		self.timeout          = timeout
		self.socket           = self._create_socket()
		self.id               = id
		self.packed_id        = struct.pack('>l', id)
		self.challenge        = None
		self.packed_challenge = struct.pack('>l', 0)
		self.retries          = 0
		self.max_retries      = retries

	def handshake(self, infinite_retries = False):
		"""
		Handshake with server to start requests. You can optionally
		ignore the previously specified retry limit.
		"""

		while self.retries < self.max_retries:
			self._send_packet(self.PACKET_TYPE_CHALLENGE)

			try:
				packet_type, id, buff = self._read_packet()
			except:
				if not infinite_retries:
					self.retries += 1
					continue

			break

		if self.retries >= self.max_retries:
			raise Exception('Unable to make handshake with server')

		self.challenge        = int(buff[:-1])
		self.packed_challenge = struct.pack('>l', self.challenge)

	def get_status(self):
		"""
		Get the server's status.
		"""

		if not self.challenge:
			self.handshake()

		self._send_packet(self.PACKET_TYPE_QUERY, self.packed_id)

		try:
			packet_type, id, buff = self._read_packet()
		except:
			self.handshake()
			return self.get_status()

		end_token_index = buff.find('\x01player_')
		key_value_pairs = buff[:end_token_index].split('\x00')
		buff            = buff[end_token_index:]

		data = dict(zip(key_value_pairs[0::2], key_value_pairs[1::2]))
		del data['']

		for key in ('hostport', 'maxplayers', 'numplayers'):
			if key in data:
				data[key] = int(data[key])

		return data

	def get_full_status(self):
		"""
		Get the server rules.
		"""

		if not self.challenge:
			self.handshake()

		self._send_packet(self.PACKET_TYPE_QUERY, self.packed_id)

		try:
			packet_type, id, buff = self._read_packet()
		except:
			self.retries += 1
			if self.retries < self.max_retries:
				self.handshake(infinite_retries = True)
				return self.get_rules()
			else:
				raise Exception('Unable to make handshake with server')

		data = {}

		buff = buff[11:]
		items, players = buff.split('\x00\x00\x01player_\x00\x00')

		if items[:8] == 'hostname':
			items = 'motd' + items[8:]

		items = items.split('\x00')
		data  = dict(zip(items[::2], items[1::2]))

		players = players[:2]

		if players:
			data['players'] = players.split('\x00')
		else:
			data['players'] = []

		for key in ('numplayers', 'maxplayers', 'hostport'):
			if key in data:
				data[key] = int(data[key])

		data['raw_plugins']               = data['plugins']
		data['software'], data['plugins'] = self._parse_plugins(data['raw_plugins'])

		return data

	def _send_raw(self, data):
		"""
		Send raw data to the server.
		"""

		self.socket.sendto(self.MAGIC_PREFIX + data, self.address)

	def _send_packet(self, packet_type, data = ''):
		"""
		Send a packet to the query server.
		"""

		self._send_raw(struct.pack('>B', packet_type) + self.packed_id + self.packed_challenge + data)

	def _read_packet(self):
		"""
		Read a packet from the server.
		"""

		buff = self.socket.recvfrom(2048)[0]

		packet_type = struct.unpack('>B', buff[0])[0]
		id          = struct.unpack('>l', buff[1:5])[0]

		return packet_type, id, buff[5:]

	def _create_socket(self):
		"""
		Create a new socket
		"""

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(self.timeout)

		return sock

	@staticmethod
	def _parse_plugins(raw_plugins):
		"""
		Parse raw plugin data
		"""

		parts   = raw_plugins.split(':', 1)
		server  = parts[0].strip()
		plugins = []

		if len(parts) == 2:
			plugins = [s.strip() for s in parts[1].split(';')]

		return server, plugins

