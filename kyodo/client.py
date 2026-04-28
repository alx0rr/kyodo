from kyodo.utils.requester import Requester
from kyodo.utils.generators import random_ascii_string
from kyodo.utils import log
from kyodo.ws import Socket
from kyodo.api import *



class Client(Socket, AuthModule, CommonModule, ChatModule, UserModule, CircleModule,
	CircleAdminModule, BlogModule):


	"""
	Main class for interacting with Kyodo servers.

	This client serves as the central point for accessing all Kyodo API features.
	It integrates HTTP requests, WebSocket connections, and user session management.

	Args:
		deviceId (str | None):
			A unique identifier for the device.
			If not provided, one will be generated automatically.
			It is recommended to keep this value consistent across sessions to avoid
			authentication or session-related issues.

		language (str):
			Language code used in API requests and responses.
			Default is 'en'.
			Examples: 'en', 'ru', 'ja'.
			Supported languages can be retrieved via:
				client.get_supported_languages() -> list[str]

		region (str):
			API region used for routing requests.
			Examples: 'eu', 'us', 'ru', 'asia'.

		user_agent (str):
			User-Agent string sent in HTTP request headers.
			Defaults to an iOS-style User-Agent but can be customized.

		timezone (str):
			IANA timezone identifier (e.g. "Europe/Oslo", "Asia/Tokyo").
			Affects how time-related data is interpreted by the server.

		socket_enable (bool):
			Enables WebSocket support for real-time communication
			such as live updates, messages, or event streaming.

		socket_trace (bool):
			Enables low-level socket debugging output.

			If True:
			- logs socket connection lifecycle events (connect, send, receive, close)
			- useful for debugging network, proxy, and WebSocket issues
			- may produce verbose output

			Recommended for development only.

		socket_daemon (bool):
			Controls whether socket background threads run as daemon threads.

			If True:
			- socket threads will not block application shutdown
			- useful for scripts, bots, and short-lived processes

			If False:
			- ensures clean shutdown of socket connections
			- recommended for long-running services

	Objects:

		Client.me (kyodo.UserProfile):
			Currently authenticated user profile.
			Available only after successful login.

		Client.account (kyodo.AccountInfo):
			Currently authenticated account information.
			Available after login.

		Client.req (kyodo.Requester):
			Internal HTTP request handler used for API communication.

	Attributes:
		socket_enable (bool):
			Indicates whether WebSocket support is enabled.
	"""


	def __init__(self, deviceId: str | None = None, language: str = 'en', region: str = "en", user_agent: str = "okhttp/4.12.0", timezone: str = "Europe/Oslo", socket_enable: bool = True, socket_trace: bool = False, socket_daemon: bool = True, proxy: str | dict | None = None):
		self.socket_enable = socket_enable

		if deviceId is None:
			deviceId = random_ascii_string(26)
			log.warning(
				f"Not providing the same device-id can lead to issues. Please grab a valid one and always use it. Also please note that the generation of device-id is experimental and may not work. We generated you this device-id: {deviceId}"
			)

		self.req = Requester(user_agent, language, region, timezone, deviceId, proxy)
		Socket.__init__(self, socket_trace, socket_daemon)


	def __str__(self):
		return f"kyodo.Client <deviceId={self.deviceId}, socket_enable={self.socket_enable}>"
	
	def __repr__(self):
		return (f"kyodo.Client(deviceId={self.req.deviceId!r}, user_agent{self.user_agent!r}, language={self.req.language!r}, "
				f"timezone={self.req.timezone!r}, socket_enable={self.socket_enable!r}, "
				f"userId={self.userId!r}, token={self.token!r})")


	def close(self):
		self.ws_disconnect()