from orjson import loads
from re import compile
from typing import Any, Callable


from .generators import _x_sig, _x_signature, strtime
from .constants import app_id, app_version

class ContentTypeError(Exception):
	"""
	ContentType found is not valid.
	"""



JSONDecoder = Callable[[str], Any]
DEFAULT_JSON_DECODER = loads
json_re = compile(r"^application/(?:[\w.+-]+?\+)?json")


def _is_expected_content_type(
	response_content_type: str, expected_content_type: str
) -> bool:
	if expected_content_type == "application/json":
		return json_re.match(response_content_type) is not None
	return expected_content_type in response_content_type




def build_headers(
	user_agent: str,
	language: str,
	timezone: str,
	deviceId: str,
	token: str | None = None,
	uid: str | None = None,
	headers: dict | None = None,
	content_type: str | None = "application/json",
	data: dict | bytes | None = None,
) -> dict:
	t = strtime()

	default_headers = {
		"User-Agent": user_agent,
		"Accept": "application/json",
		"app-id": app_id,
		"app-version": app_version,
		"device-language": language,
		"device-timezone": timezone,
		"Accept-Language": language,
		"start-time": t,
		"device-id": deviceId,
		"x-signature": _x_signature(deviceId, int(t)),
	}

	if content_type:
		default_headers["Content-Type"] = content_type

	if token:
		default_headers["Authorization"] = token
		if uid:
			default_headers["x-sig"] = _x_sig(
				deviceId, uid, t, data or {}
			)

	if headers:
		default_headers.update(headers)

	return default_headers


class HTTPRequest:
	def __init__(
		self,
		method: str,
		url: str,
		body: str | dict | bytes | None,
		headers: dict | None,
		proxy: str | dict | None,
	):
		
		self.method = method
		self.url = url
		self.body = body
		self.headers = headers
		self.proxy = proxy

class AsyncHTTPResponse:

	def __init__(
		self,
		*,
		status: int,
		body: bytes,
		headers: dict,
		url: str,
		method: str,
		encoding: str,
		request: HTTPRequest
	):
		self.status = status
		self._body = body
		self.headers = headers
		self.url = url
		self.method = method
		self.encoding = encoding
		self.request = request


	async def get_bytes(self) -> bytes:
		return self._body 

	async def text(self, encoding: str | None = None, errors: str = "strict") -> str:
		"""Read response payload and decode."""

		if encoding is None:
			encoding = self.encoding
		return self._body.decode(encoding, errors=errors)

	async def json(
		self,
		*,
		encoding: str | None = None,
		loads: JSONDecoder = DEFAULT_JSON_DECODER,
		content_type: str = "application/json",
	) -> Any:
		"""Read and decodes JSON response."""

		if content_type:
			ctype = self.headers.get("Content-Type", "").lower()
			if not _is_expected_content_type(ctype, content_type):
				raise ContentTypeError(
						"Attempt to decode JSON with unexpected mimetype: %s" % ctype
				)

		stripped = self._body.strip()
		if not stripped:
			return None
		if encoding is None:
			encoding = self.encoding
		return loads(stripped.decode(encoding))