from .exceptions import checkException
from . import log
from .generators import _x_sig, _x_signature, random_ascii_string, strtime
from .constants import api_url, app_id, app_version

from aiohttp import ClientSession, ClientResponse
from orjson import dumps

class Requester:
	"""
	Main class for handling HTTPS requests in the Kyodo API library.

	This class is responsible for making HTTP requests to the Kyodo servers, managing headers, and providing 
	convenience methods for interaction with the API

	### Args:

		user_agent (str): 
			The User-Agent string sent in HTTP requests. It identifies the client software making the request.
		
		language (str): 
			The language code used for API requests and responses. It influences the language in which the responses are returned.
		
		timezone (str): 
			The timezone string (e.g., "Europe/Oslo", "Asia/Tokyo"). This may affect how dates and times are formatted and returned by the server.
		
		deviceId (str | None, optional): 
			A unique identifier for the device. If not provided, it will be generated.
	
	### Attributes:	
		user_agent (str): 
			The User-Agent string used in HTTP request headers.
		
		language (str): 
			The language used for API communication.
		
		timezone (str): 
			The timezone setting used in API requests.
		
		deviceId (str | None): 
			The device identifier.

	This class is used internally by the `Client` to manage HTTP requests and communicate with Kyodo servers.
	"""
	
	def __init__(self, __uid, user_agent: str, language: str, timezone: str, deviceId: str | None = None, proxy: str | None = None):
		self.user_agent: str = user_agent
		self.timezone: str = timezone
		self.language: str = language
		self.token: str = None
		self.proxy: str = proxy
		self.deviceId: str = deviceId or random_ascii_string(26)
		self.__uid = __uid


	def headers(self, headers: dict = None, content_type: str = "application/json", data: dict | None = None) -> dict:
		t = strtime()

		default_headers = {
			"user-agent": self.user_agent,
			"Accept": "application/json",
			"app-id": app_id,
			"app-version": app_version,
			"device-language": self.language,
			"device-timezone": self.timezone,
			"Accept-Language": self.language,
			"start-time": t,
			"device-id": self.deviceId,
			"x-signature":_x_signature( self.deviceId, int(t)),
		}
		if content_type: default_headers["content-type"] = content_type
		if self.token:
			default_headers["Authorization"] = self.token
			uid =  self.__uid()
			if not uid:
				log.warning("No UID found! 'X-Sig' header will be missing.")
			else:
				default_headers["x-sig"] = _x_sig(
					self.deviceId, uid, t, data or {}
				)

		if headers: default_headers.update(headers)
		return default_headers


	async def make_async_request(self, method: str, endpoint: str = None, body: dict | bytes = None, allowed_code: int = 200, headers: dict = None , api: str = None) -> ClientResponse:
		async with ClientSession() as asyncSession:
			data = dumps(body) if isinstance(body, dict) else body if body is not None else None
			headers = self.headers(headers, data=body)
			response = await asyncSession.request(method, f"{api or api_url}{endpoint or ''}", data=data, headers=headers, proxy=self.proxy)
			print(await response.text())
			await asyncSession.close()
			log.debug(f"[https][{method}][{endpoint or ''}][{response.status}]: {len(body) if isinstance(body, bytes) else body}")
			return checkException(await response.text()) if response.status != allowed_code else response