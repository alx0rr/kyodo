from kyodo.utils.requester import Requester
from kyodo.utils.generators import random_ascii_string
from kyodo.utils import log
from kyodo.ws._async import Socket
from kyodo.api._async import *

from asyncio import sleep


class Client(
	Socket, AuthModule, CommonModule, ChatModule, UserModule, CircleModule,
	CircleAdminModule, BlogModule):
	"""
	Main async class for interacting with Kyodo servers.

	This client serves as the central point for accessing all Kyodo API features.
	It inherits functionality from various modules and provides access to user session, sockets, and HTTP requests.

	Args:
		deviceId (str | None): 
			A unique identifier for the device. If not provided, one will be generated randomly.
			It is recommended to use a consistent device ID to avoid issues with authentication and sessions.

		language (str): 
			Language code used in API requests and responses. Default is 'en'.
			Examples: 'en', 'ru', 'ja'.
			You can view supported languages with:
				client.get_supported_languages() -> list[str]
		region (str):
			api requests region
			Examples: 'en', 'ru', 'ja'.

		user_agent (str): 
			User-Agent string sent in HTTP request headers.
			Defaults to an iOS-style string, but can be customized as needed.

		timezone (str): 
			Timezone in IANA format (e.g., "Europe/Oslo", "Asia/Tokyo").
			May influence how timestamps are processed on the server.

		socket_enable (bool): 
			Enables real-time socket communication if True (e.g., for receiving live messages or updates).

	Objects:
		- Client.me (kyodo.UserProfile): 
			The currently authenticated user's profile. Available after login.

		- Client.account (kyodo.AccountInfo)
			The currently authenticated user's account info. Available after login.

		- Client.req (kyodo.Requester): 
			Internal request handler for making HTTP requests to the API.

	Attributes:
		- socket_enable (bool): 
			Whether socket support is enabled for real-time features.
	"""


	def __init__(self, deviceId: str | None = None, language: str = 'en', region: str = "en", user_agent: str = "okhttp/4.12.0", timezone: str = "Europe/Oslo", socket_enable: bool = True, proxy: str | None = None):
		self.socket_enable = socket_enable

		if deviceId is None:
			deviceId = random_ascii_string(26)
			log.warning(
				f"Not providing the same device-id can lead to issues. Please grab a valid one and always use it. Also please note that the generation of device-id is experimental and may not work. We generated you this device-id: {deviceId}"
			)

		self.req = Requester(user_agent, language, region, timezone, deviceId, proxy)
		Socket.__init__(self)


	def __str__(self):
		return f"kyodo.AsyncClient <deviceId={self.deviceId}, socket_enable={self.socket_enable}>"
	
	def __repr__(self):
		return (f"kyodo.AsyncClient(deviceId={self.req.deviceId!r}, user_agent{self.user_agent!r}, language={self.req.language!r}, "
				f"timezone={self.req.timezone!r}, socket_enable={self.socket_enable!r}, "
				f"userId={self.userId!r}, token={self.token!r})")


	async def close(self):
		await sleep(1)
		await self.ws_disconnect()