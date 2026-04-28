from aiohttp import ClientSession
from httpx import Client

import httpx
from orjson import dumps

from kyodo.utils.exceptions import checkException, checkAsyncException
from kyodo.utils import log
from kyodo.utils.generators import random_ascii_string
from kyodo.utils.constants import api_url
from kyodo.utils.request_helper import AsyncHTTPResponse, HTTPResponse, HTTPRequest, build_headers



class Requester:
	"""
	Main class for handling HTTPS requests in the Kyodo API library.
	"""

	def __init__(
		self,
		user_agent: str,
		language: str,
		region: str,
		timezone: str,
		deviceId: str | None = None,
		proxy: str | dict | None = None,
	):
		self.user_agent: str = user_agent
		self.timezone: str = timezone
		self.region: str = region
		self.language: str = language
		self.token: str | None = None
		self.proxy: str | None = proxy
		self.deviceId: str = deviceId or random_ascii_string(26)



	def make_request(
		self,
		method: str,
		endpoint: str | None = None,
		body: dict | bytes | None = None,
		allowed_code: int | list[int] = 200,
		headers: dict | None = None,
		api: str | None = None,
	) -> HTTPResponse:

		data = dumps(body) if isinstance(body, dict) else body

		req_headers = build_headers(
			self.user_agent,
			self.language,
			self.region,
			self.timezone,
			self.deviceId,
			self.token,
			headers
		)

		url = f"{api or api_url}{endpoint or ''}"

		with Client() as session:

			resp = session.request(
				method,
				url,
				content=data,
				headers=req_headers,
			)

			response = HTTPResponse(
				status=resp.status_code,
				body=resp.content,
				headers=dict(resp.headers),
				url=str(resp.url),
				method=method,
				encoding=resp.encoding,
				request=HTTPRequest(
					method,
					url,
					data,
					req_headers,
					self.proxy
				)
			)

			log.debug(
				f"[https][{method}][{endpoint or ''}][{resp.status_code}]: "
				f"{len(body) if isinstance(body, bytes) else body or '{}'}\n"
				f"Headers: {req_headers}"
			)

			if isinstance(allowed_code, int):
				allowed_code = [allowed_code]

			if resp.status_code not in allowed_code:
				checkException(response)

			return response






	async def make_async_request(
		self,
		method: str,
		endpoint: str | None = None,
		body: dict | bytes | None = None,
		allowed_code: int | list[int] = 200,
		headers: dict | None = None,
		api: str | None = None,
	) -> AsyncHTTPResponse:
		data = dumps(body) if isinstance(body, dict) else body
		req_headers = build_headers(
			self.user_agent,
			self.language,
			self.region,
			self.timezone,
			self.deviceId,
			self.token,
			headers)


		url = f"{api or api_url}{endpoint or ''}"

		async with ClientSession() as session:
			async with session.request(
				method,
				url,
				data=data,
				headers=req_headers,
				proxy=self.proxy,
			) as response:
				response = AsyncHTTPResponse(
					status=response.status,
					body=await response.read(),
					headers=dict(response.headers),
					url=str(response.url),
					method=method,
					encoding=response.get_encoding(),
					request=HTTPRequest(
						method,
						url,
						data,
						req_headers,
						self.proxy if isinstance(self.proxy, str) else None

					)
				)

				log.debug(
					f"[https][{method}][{api or ''}{endpoint or ''}][{response.status}]: "
					f"{len(body) if isinstance(body, bytes) else body or '{}'}\n"
					f"Headers: {req_headers}"
				)

				if isinstance(allowed_code, int):
					allowed_code=[allowed_code]

				if response.status not in allowed_code:
					await checkAsyncException(response)
					
				return response
