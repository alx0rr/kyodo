from kyodo.api.base import BaseClass
from kyodo.utils import require_auth
from kyodo.utils.exceptions import ArgumentNeeded, EmailInUse, UsernameTaken
from kyodo.utils.generators import decode_auth_token
from kyodo.objects import AccountInfo, UserProfile, BirthdayInfo

class AuthModule(BaseClass):

	async def login(self, email: str, password: str) -> UserProfile:
		if self.token: return self.me
		response = await self.req.make_async_request("POST", "/g/s/auth/login", {
			"type": 0,
			"email": email,
			"secret": password
		})
		data: dict = await response.json()
		self.req.token  = data.get("token")
		if self.socket_enable:await self.ws_connect()
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))
		return self.me
	
	async def login_token(self, token: str, refresh_token: bool = False) -> UserProfile:
		if refresh_token:return await self.refresh_token(token)
		token_info = decode_auth_token(token)
		self.req.token = token
		self.me.userId = token_info.id
		self.me.role = token_info.role
		self.me.premiumType = token_info.premium_type

		self.account.userId = token_info.id
		self.account.email = token_info.email
		self.account.premiumType = token_info.premium_type

		if self.socket_enable: await self.ws_connect()
		return self.me

	async def refresh_token(self, token: str | None = None) -> UserProfile:
		if not token and not self.req.token: raise ArgumentNeeded("token: None")

		response = await self.req.make_async_request("POST", "/g/s/auth/login", {
		  "type": 1,
		  "token": self.req.token if self.req.token else token
		})
		data: dict = await response.json()
		self.req.token = data.get("token")
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))
		
		if self.socket_enable:
			await self.ws_disconnect()
			await self.ws_connect()
		return self.me

	@require_auth
	async def logout(self) -> bool:
		await self.req.make_async_request("POST", "/g/s/auth/logout")
		self.req.token = None
		self.account = AccountInfo({})
		self.me = UserProfile({})
		if self.socket_enable: await self.ws_disconnect()
		return  True




	async def email_available_check(self, email: str) -> bool:
		try:
			await self.req.make_async_request("POST", f"/g/s/auth/email-available-check", {"email": email})
			return True
		except EmailInUse:return False

	async def username_available_check(self, username: str) -> bool:
		try:
			await self.req.make_async_request("POST", f"/g/s/auth/username-check", {"username": username})
			return True
		except UsernameTaken:return False


	async def request_reset_password_code(self, email: str):
		await self.req.make_async_request("POST", "/g/s/auth/reset-password", {"email": email})

	async def reset_password(self, email: str, code: int):
		await self.req.make_async_request("POST", "/g/s/auth/reset-password/confirm", {"email": email, "verificationCode": code})

	
	@require_auth
	async def change_password(self, old_password: str, new_password: str) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/g/s/auth/otp/send-email-verification", {
			"secret1": old_password,
			"secret2": new_password
		})
		data: dict = await response.json()
		self.req.token = data.get("token")
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))

		return self.me



	async def check_age(self, birthday: str = "Sun Apr 04 2004 02:00:00 GMT+0200") -> BirthdayInfo:
		response = await self.req.make_async_request("POST", f"/g/s/auth/age-check", {"birthday": birthday})
		return BirthdayInfo((await response.json()).get("birthdayInfo", {}))


	async def request_email_verification_code(self, email: str):
		await self.req.make_async_request("POST", f"/g/s/auth/otp/send-email-verification", {"email": email})

	async def email_verification(self, email: str, code: int):
		await self.req.make_async_request("POST", f"/g/s/auth/otp/email-verification", {"email": email, "verificationCode": code})
	

	async def register(self, email: str, password: str, username: str, turnstileToken: str, birthday: str = "Sun Apr 04 2004 02:00:00 GMT+0200") -> UserProfile:
		response = await self.req.make_async_request("POST", "/g/s/auth/register", {
			"email": email,
			"secret": password,
			"birthday": birthday,
			"username": username,
			"turnstileToken": turnstileToken
		})
		data: dict = await response.json()
		self.req.token  = data.get("token")
		if self.socket_enable:await self.ws_connect()
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))
		return self.me