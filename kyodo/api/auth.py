from .base import BaseClass
from ..objects import BaseProfile
from ..utils import require_auth

class AuthModule(BaseClass):

	async def login(self, email: str, password: str) -> BaseProfile:
		"""
		after use client.email_2fa_auth
		"""
		if self.token: return self.me
		response = await self.req.make_async_request("POST", "/g/s/auth/login", {
			"type": 0,
			"email": email,
			"password": password
		})
		data: dict = await response.json()
		self.req.token  = data.get("apiToken")
		if self.socket_enable:await self.ws_connect()
		self.me = BaseProfile(data.get("apiUser"))

		return self.me

	async def login_token(self, token: str, userId: str | None, refresh: bool = False) -> bool:
		self.req.token = token
		self.me.userId = userId
		if refresh: await self.refresh_token()
		if self.socket_enable:await self.ws_connect()
		return True

	@require_auth
	async def logout(self) -> bool:
		await self.req.make_async_request("POST", "/g/s/auth/logout")
		self.req.token = None
		if self.socket_enable: await self.ws_disconnect()
		return  True



	async def email_2fa_auth(self, userId: str, deviceId: str, token: str) -> bool:
		await self.req.make_async_request("POST", api="https://kyodo.app/account/2fa-email", body={
			"accountId": userId,
			"token": token,
			"deviceId": deviceId
		})
		return True

	@require_auth
	async def refresh_token(self) -> str:
		response = await self.req.make_async_request("POST", "/g/s/auth/login", {
		  "type": 1  
		})
		data: dict = await response.json()
		self.req.token = data.get("apiToken")
		return self.req.token
	

