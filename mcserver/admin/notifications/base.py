import abc

class AdminNotificationInterface(object):
	"""
	Interface for things that care about admin type updates
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self, **kwargs):
		"""
		Create interface object with config
		"""

	@abc.abstractmethod
	def server_start(self, server):
		"""
		Called when the server is started. This call is made after the server is
		started and only on success.
		"""

	# TODO: server_start_fail

	@abc.abstractmethod
	def server_stop(self, server):
		"""
		Called when the server is stopped. This call is made after the server is
		stopped and only on success.
		"""

	# TODO: server_stop_fail

	@abc.abstractmethod
	def server_restart(self, server):
		"""
		Called when the server is restarted. this call is made after the server
		is restarted and only on success.
		"""

	# TODO: server_restart_fail

