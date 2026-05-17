from kyodo.utils.requester import Requester
from kyodo.utils.generators import random_ascii_string
from kyodo.utils import log
from kyodo.ws import Socket
from kyodo.api import *
from kyodo.objects.args import ProxyConfig, ProxyPool
from kyodo.utils.state import ThreadSafeState


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
			Examples: 'eu', 'ja', 'ru'.

		user_agent (str):
			User-Agent string sent in HTTP request headers.
			Can be customized.

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
			
		proxy (ProxyConfig | ProxyPool | None):
			Proxy configuration for all outgoing connections (HTTP and WebSocket).
			Accepts a single proxy or a pool of proxies for rotation.

			Supported proxy types:
				- HTTP  — standard HTTP proxy
				- SOCKS4 — SOCKS4 proxy
				- SOCKS5 — SOCKS5 proxy (recommended, supports auth and IPv6)

			Single proxy:
				proxy = ProxyConfig(host="1.2.3.4", port=1080, proxy_type=ProxyType.SOCKS5)
				proxy = ProxyConfig.from_url("socks5://user:pass@1.2.3.4:1080")

			Proxy pool (random proxy is picked per request):
				pool = ProxyPool()
				pool.add(ProxyConfig.from_url("http://1.2.3.4:8080"))
				pool.add(ProxyConfig.from_url("socks5://1.2.3.4:1080"))

			Usage flags (optional, controls where proxy is applied):
				ProxyConfig.from_url("http://1.2.3.4:8080", usage=ProxyUsage.HTTP)  # HTTP only
				ProxyConfig.from_url("socks5://1.2.3.4:1080", usage=ProxyUsage.WS)  # WS only
				ProxyConfig.from_url("socks5://1.2.3.4:1080", usage=ProxyUsage.ALL) # everywhere (default)

			Default is None (no proxy).

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

	req: Requester
	state = ThreadSafeState()

	@property
	def proxy(self) -> ProxyConfig | ProxyPool | None:
		return self.req.proxy


	def set_proxy(self, proxy: ProxyConfig | ProxyPool | None):
		self.req.proxy = proxy

	def __init__(self, deviceId: str | None = None, language: str = 'en', region: str = "en", user_agent: str = "okhttp/4.12.0", timezone: str = "Europe/Oslo", socket_enable: bool = True, socket_trace: bool = False, socket_daemon: bool = True, proxy: ProxyConfig | ProxyPool | None = None):
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