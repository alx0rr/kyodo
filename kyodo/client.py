from .utils.requester import Requester
from .utils.generators import random_ascii_string
from .utils import log
from .ws import Socket
from .api import *

class Client(
	AuthModule, AccountModule, ChatsModule, CirclesModule,
	StickersModule, UsersModule, CommonModule, PostsModule,
	StoreModule):
	"""
	Main class for interacting with Kyodo servers.

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

		user_agent (str): 
			User-Agent string sent in HTTP request headers.
			Defaults to an iOS-style string, but can be customized as needed.

		timezone (str): 
			Timezone in IANA format (e.g., "Europe/Oslo", "Asia/Tokyo").
			May influence how timestamps are processed on the server.

		socket_enable (bool): 
			Enables real-time socket communication if True (e.g., for receiving live messages or updates).


	Modules:
		This class includes methods from the following modules:
		- AuthModule       : Login, logout, token management, and related features.
		- AccountModule    : Account settings, email/password reset, and profile updates.
		- ChatsModule      : Chat features such as sending and managing messages.
		- CirclesModule    : Circle (group) management and interaction.
		- StickersModule   : Sticker management and usage.
		- UsersModule      : User-related actions, including member lists and blocking.
		- CommonModule     : Miscellaneous common-purpose API methods.
		- PostsModule      : Managing posts and post folders.

	Objects:
		- Client.me (kyodo.BaseProfile): 
			The currently authenticated user's profile. Available after login.

		- Client.req (kyodo.Requester): 
			Internal request handler for making HTTP requests to the API.

	Attributes:
		
		- socket_enable (bool): 
			Whether socket support is enabled for real-time features.
	Properties:
		- language (str): 
			The current language used for API communication.

		- user_agent (str): 
			The current User-Agent string.

		- timezone (str): 
			The current timezone setting.

		- token (str): 
			The session token used for authorized requests (available after login).

		- deviceId (str): 
			The unique identifier used to represent the client device.
	"""


	def __init__(self, deviceId: str | None = None, language: str = 'en', user_agent: str = "Kyodo/135 CFNetwork/1496.0.7 Darwin/23.5.0", timezone: str = "Europe/Oslo", socket_enable: bool = True, proxy: str | None = None):
		self.socket_enable = socket_enable

		if deviceId is None:
			deviceId = random_ascii_string(26)
			log.warning(
				f"Not providing the same device-id can lead to issues. Please grab a valid one and always use it. Also please note that the generation of device-id is experimental and may not work. We generated you this device-id: {deviceId}"
			)

		self.req = Requester(self.__get_uid, user_agent, language, timezone, deviceId, proxy)
		Socket.__init__(self)


	def __str__(self):
		return f"kyodo.Client <deviceId={self.deviceId}, socket_enable={self.socket_enable}>"
	
	def __repr__(self):
		return (f"kyodo.Client(deviceId={self.req.deviceId!r}, user_agent{self.user_agent!r}, language={self.req.language!r}, "
				f"timezone={self.req.timezone!r}, socket_enable={self.socket_enable!r}, "
				f"userId={self.userId!r}, token={self.token!r})")
	

	def __get_uid(self) -> str | None:
		return self.userId