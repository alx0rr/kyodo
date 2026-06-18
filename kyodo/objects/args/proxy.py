from __future__ import annotations
from enum import Enum, Flag, auto
from dataclasses import dataclass, field
from aiohttp_socks import ProxyConnector, ProxyType as SocksProxyType
from typing import Optional
from random import choice


class ProxyType(str, Enum):
	HTTP   = "http"
	SOCKS4 = "socks4"
	SOCKS5 = "socks5"


class ProxyUsage(Flag):
	HTTP = auto()   # sync/async HTTP
	WS   = auto()   # sync/async WebSocket
	ALL  = HTTP | WS


@dataclass
class ProxyConfig:
	host: str
	port: int
	proxy_type: ProxyType    = ProxyType.HTTP
	username:   Optional[str] = None
	password:   Optional[str] = None
	usage:      ProxyUsage   = ProxyUsage.ALL

	@property
	def _auth(self) -> str:
		if self.username and self.password:
			return f"{self.username}:{self.password}@"
		return ""

	@property
	def url(self) -> str:
		return f"{self.proxy_type.value}://{self._auth}{self.host}:{self.port}"

	def allows(self, usage: ProxyUsage) -> bool:
		return bool(self.usage & usage)

	@classmethod
	def from_url(cls, url: str, usage: ProxyUsage = ProxyUsage.ALL) -> "ProxyConfig":
		from urllib.parse import urlparse
		parsed = urlparse(url)
		return cls(
			host=parsed.hostname,
			port=parsed.port,
			proxy_type=ProxyType(parsed.scheme.lower()),
			username=parsed.username or None,
			password=parsed.password or None,
			usage=usage,
		)

	def for_aiohttp(self, isWS: bool = False) -> str | None:
		if not self.allows(ProxyUsage.HTTP) and not isWS:
			return None
		if self.proxy_type == ProxyType.HTTP:
			return self.url
		return None

	def for_aiohttp_connector(self, usage: ProxyUsage = ProxyUsage.ALL):
		if not self.allows(usage):
			return None
		_map = {
			ProxyType.HTTP:   SocksProxyType.HTTP,
			ProxyType.SOCKS4: SocksProxyType.SOCKS4,
			ProxyType.SOCKS5: SocksProxyType.SOCKS5,
		}
		return ProxyConnector(
			proxy_type=_map[self.proxy_type],
			host=self.host,
			port=self.port,
			username=self.username,
			password=self.password,
		)

	def for_httpx(self) -> str | None:
		if not self.allows(ProxyUsage.HTTP):
			return None
		return self.url

	def for_websocket(self) -> dict | None:
		if not self.allows(ProxyUsage.WS):
			return None
		base = {
			"http_proxy_host": self.host,
			"http_proxy_port": self.port,
			"proxy_type":      self.proxy_type.value,
		}
		if self.username:
			base["http_proxy_auth"] = (self.username, self.password)
		return base

	def __repr__(self):
		auth = f"{self.username}:***@" if self.username else ""
		return f"<ProxyConfig {self.proxy_type.value}://{auth}{self.host}:{self.port} usage={self.usage}>"


@dataclass
class ProxyPool:
	proxies: list[ProxyConfig] = field(default_factory=list)

	def add(self, proxy: ProxyConfig) -> "ProxyPool":
		self.proxies.append(proxy)
		return self

	def random(self, usage: ProxyUsage = ProxyUsage.ALL) -> Optional[ProxyConfig]:
		filtered = [p for p in self.proxies if p.allows(usage)]
		return choice(filtered) if filtered else None

	def __iter__(self):
		return iter(self.proxies)

	def __len__(self):
		return len(self.proxies)