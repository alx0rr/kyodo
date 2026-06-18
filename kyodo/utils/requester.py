from __future__ import annotations

from aiohttp import ClientSession
from httpx import Client
from orjson import dumps

from kyodo.utils.exceptions import checkException, checkAsyncException
from kyodo.utils import log
from kyodo.utils.generators import random_ascii_string
from kyodo.utils.constants import api_url
from kyodo.utils.request_helper import AsyncHTTPResponse, HTTPResponse, HTTPRequest, build_headers, resolve_proxy
from kyodo.objects.args import ProxyConfig, ProxyPool, ProxyType, ProxyConnector, ProxyUsage


class Requester:
    """Main class for handling HTTPS requests in the Kyodo API library."""

    def __init__(
        self,
        user_agent: str,
        language: str,
        region: str,
        timezone: str,
        deviceId: str | None = None,
        proxy: ProxyConfig | ProxyPool | None = None,
    ):
        self.user_agent: str = user_agent
        self.timezone: str = timezone
        self.region: str = region
        self.language: str = language
        self.token: str | None = None
        self.proxy: ProxyConfig | ProxyPool | None = proxy
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
            self.user_agent, self.language, self.region,
            self.timezone, self.deviceId, self.token, headers
        )
        url = f"{api or api_url}{endpoint or ''}"

        _proxy = resolve_proxy(self.proxy, ProxyUsage.HTTP)
        proxies = _proxy.for_httpx() if _proxy else None

        with Client(proxy=proxies) as session:
            resp = session.request(method, url, content=data, headers=req_headers)
            response = HTTPResponse(
                status=resp.status_code,
                body=resp.content,
                headers=dict(resp.headers),
                url=str(resp.url),
                method=method,
                encoding=resp.encoding,
                request=HTTPRequest(method, url, data, req_headers, _proxy)
            )
            log.debug(
                f"[https][{method}][{endpoint or ''}][{resp.status_code}]: "
                f"{len(body) if isinstance(body, bytes) else body or '{}'}\n"
                f"Headers: {req_headers}\n"
                f"Proxy: {_proxy.url if _proxy else 'No proxy'}"
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
            self.user_agent, self.language, self.region,
            self.timezone, self.deviceId, self.token, headers
        )
        url = f"{api or api_url}{endpoint or ''}"

        _proxy = resolve_proxy(self.proxy, ProxyUsage.HTTP)
        connector: ProxyConnector | None = None
        proxy_url: str | None = None

        if _proxy:
            if _proxy.proxy_type == ProxyType.HTTP:
                proxy_url = _proxy.for_aiohttp()
            else:
                connector = _proxy.for_aiohttp_connector()  # SOCKS4/5

        async with ClientSession(connector=connector) as session:
            async with session.request(
                method, url, data=data, headers=req_headers, proxy=proxy_url
            ) as resp:
                response = AsyncHTTPResponse(
                    status=resp.status,
                    body=await resp.read(),
                    headers=dict(resp.headers),
                    url=str(resp.url),
                    method=method,
                    encoding=resp.get_encoding(),
                    request=HTTPRequest(method, url, data, req_headers, _proxy)
                )
                log.debug(
                    f"[https][{method}][{api or ''}{endpoint or ''}][{response.status}]: "
                    f"{len(body) if isinstance(body, bytes) else body or '{}'}\n"
                    f"Headers: {req_headers}\n"
                    f"Proxy: {_proxy.url if _proxy else 'No proxy'}"
                )
                if isinstance(allowed_code, int):
                    allowed_code = [allowed_code]
                if response.status not in allowed_code:
                    await checkAsyncException(response)
                return response