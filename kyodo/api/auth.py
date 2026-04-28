from kyodo.api.base import SyncBaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.utils.exceptions import ArgumentNeeded, EmailInUse, UsernameTaken
from kyodo.utils.generators import decode_auth_token
from kyodo.objects import AccountInfo, UserProfile, BirthdayInfo

class AuthModule(SyncBaseClass):

	def login(self, email: str, password: str) -> UserProfile:
		if self.token: return self.me
		response = self.req.make_request("POST", "/g/s/auth/login", {
			"type": 0,
			"email": email,
			"secret": password
		})
		data: dict = response.json()
		self.req.token  = data.get("token")
		if self.socket_enable: self.ws_connect()
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))
		return self.me
	
	def login_token(self, token: str, refresh_token: bool = False) -> UserProfile:
		if refresh_token:return self.refresh_token(token)
		token_info = decode_auth_token(token)
		self.req.token = token
		self.me.userId = token_info.id
		self.me.role = token_info.role
		self.me.premiumType = token_info.premium_type

		self.account.userId = token_info.id
		self.account.email = token_info.email
		self.account.premiumType = token_info.premium_type

		if self.socket_enable: self.ws_connect()
		return self.me

	def refresh_token(self, token: str | None = None) -> UserProfile:
		if not token and not self.req.token: raise ArgumentNeeded("token: None")

		response = self.req.make_request("POST", "/g/s/auth/login", {
		  "type": 1,
		  "token": self.req.token if self.req.token else token
		})
		data: dict = response.json()
		self.req.token = data.get("token")
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))
		
		if self.socket_enable:
			self.ws_disconnect()
			self.ws_connect()
		return self.me

	@require_auth
	def logout(self):
		self.req.make_request("POST", "/g/s/auth/logout")
		self.req.token = None
		self.account = AccountInfo({})
		self.me = UserProfile({})
		if self.socket_enable: self.ws_disconnect()



	@require_auth
	@require_uid
	def delete_account(self, email: str):
		self.req.make_request("POST", f"/g/s/accounts/{self.userId}/deletion")




	def email_available_check(self, email: str) -> bool:
		try:
			self.req.make_request("POST", f"/g/s/auth/email-available-check", {"email": email})
			return True
		except EmailInUse:return False

	def username_available_check(self, username: str) -> bool:
		try:
			self.req.make_request("POST", f"/g/s/auth/username-check", {"username": username})
			return True
		except UsernameTaken:return False


	def request_reset_password_code(self, email: str):
		self.req.make_request("POST", "/g/s/auth/reset-password", {"email": email})

	def reset_password(self, email: str, code: int):
		self.req.make_request("POST", "/g/s/auth/reset-password/confirm", {"email": email, "verificationCode": code})

	
	@require_auth
	def change_password(self, old_password: str, new_password: str) -> UserProfile:
		response = self.req.make_request("POST", f"/g/s/auth/otp/send-email-verification", {
			"secret1": old_password,
			"secret2": new_password
		})
		data: dict = response.json()
		self.req.token = data.get("token")
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))

		return self.me



	def check_age(self, birthday: str = "Sun Apr 04 2004 02:00:00 GMT+0200") -> BirthdayInfo:
		response = self.req.make_request("POST", f"/g/s/auth/age-check", {"birthday": birthday})
		return BirthdayInfo(response.json().get("birthdayInfo", {}))


	def request_email_verification_code(self, email: str):
		self.req.make_request("POST", f"/g/s/auth/otp/send-email-verification", {"email": email})

	def email_verification(self, email: str, code: int):
		self.req.make_request("POST", f"/g/s/auth/otp/email-verification", {"email": email, "verificationCode": code})
	

	def register(self, email: str, password: str, username: str, turnstileToken: str, birthday: str = "Sun Apr 04 2004 02:00:00 GMT+0200") -> UserProfile:
		response = self.req.make_request("POST", "/g/s/auth/register", {
			"email": email,
			"secret": password,
			"birthday": birthday,
			"username": username,
			"turnstileToken": turnstileToken
		})
		data: dict = response.json()
		self.req.token  = data.get("token")
		if self.socket_enable:self.ws_connect()
		self.account = AccountInfo(data.get("account"))
		self.me = UserProfile(data.get("userProfile"))
		return self.me