from .base import BaseClass
from ..objects import (
	ReferralCode, Topic, HandleInfo, BaseProfile,
	AccountConfig
)
from ..utils import require_auth, exceptions, require_uid
from ..utils.generators import date_string_to_timestamp_ms

class AccountModule(BaseClass):


	async def register(self, email: str, password: str, username: str, stt: str, invite_code: str | None = None) -> tuple[str, BaseProfile]:
		#stt - idk
		result = await self.req.make_async_request("POST", "/g/s/auth/register", {
		  "email": email,
		  "password": password,
		  "handle": username,
		  "referralInviteCode": invite_code or "",
		  "stt": stt
		})
		data: dict = await result.json()
		profile = BaseProfile(data.get("apiUser"))
		return data.get("apiToken"), profile		

	@require_auth
	async def get_account_config(self) -> AccountConfig:
		result = await self.req.make_async_request("GET", "/g/s/accounts/config")
		data: dict = await result.json()
		return AccountConfig(data.get("config"))


	@require_auth
	async def set_account_birthday(self, date_string: str | None = "12.04.2003", timestamp_ms: int | None = None) -> bool:
		if not date_string and not timestamp_ms:raise exceptions.ArgumentNeeded(
			"Please enter the date in string format (12.04.2003) or in timestamp format (1050105600000)"
		)
		await self.req.make_async_request("POST", "/g/s/accounts/birthday", {
			"birthday": timestamp_ms if timestamp_ms else date_string_to_timestamp_ms(date_string)
		})
		return True


	@require_auth
	@require_uid
	async def delete_accounts(self, stt: str) -> bool:
		#stt - idk
		await self.req.make_async_request("POST", "/g/s/accounts/deletion/request", {
		  "uid": self.me.userId,
		  "stt": stt
		})

		return True
	

	@require_auth
	async def change_password(self, old: str, new: str) -> bool:
		await self.req.make_async_request("POST", "/g/s/accounts/change-password", {
				"current": old,
				"new": new
			}
		)
		return True


	@require_auth
	async def send_change_email_request(self, new_email: str, password: str) -> bool:
		"""
		after use client.verify_email
		"""
		await self.req.make_async_request("POST", "/g/s/accounts/change-email", {
			"email": new_email,
			"password": password
		})
		return True

	async def send_forgot_password_request(self, email: str) -> bool:
		"""
		after use client.verify_password_reset
		"""
		await self.req.make_async_request("POST", "/g/s/auth/forgot-password", {"email": email})
		return True

	async def verify_email(self, userId: str, token: str) -> bool:
		await self.req.make_async_request("POST", api="https://kyodo.app/account/verify-email", body={
			"accountId": userId,
			"token": token,
		})
		return True

	async def verify_password_reset(self, userId: str, token: str) -> bool:
		await self.req.make_async_request("POST", api="https://kyodo.app/account/verify-password-reset", body={
			"accountId": userId,
			"token": token,
		})
		return True
	
	async def check_email_exsist(self, email: str) -> bool:
		response = await self.req.make_async_request("POST", "/g/s/accounts/email-check", {
			"email": email
		})
		data: dict = await response.json()
		return data.get("exists")


	async def check_username_in_use(self, username: str) -> HandleInfo:
		try:
			response = await self.req.make_async_request("GET", f"/g/s/accounts/handles/{username}")
			return HandleInfo(await response.json())
		except exceptions.NotFoundError:
			return HandleInfo({"inUse": False})

	@require_auth
	async def resend_verification_email(self) -> bool:
		await self.req.make_async_request("POST", f"/g/s/auth/resend-verification-email")
		return True
	

	@require_auth
	async def edit_account_username(self, username: str) -> bool:
		await self.req.make_async_request("POST", "/g/s/accounts/handle", {"handle": username})
		return True

	#topics--------------------

	@require_auth
	async def get_my_topics(self) -> list[Topic]:
		result = await self.req.make_async_request("GET", f"/g/s/rcmd/topics?type=mine")
		data: dict =  await result.json()
		return [Topic(topic) for topic in data.get("topics", [])]

	@require_auth
	async def get_all_topics(self) -> list[Topic]:
		result = await self.req.make_async_request("GET", f"/g/s/rcmd/topics?type=all")
		data: dict =  await result.json()
		return [Topic(topic) for topic in data.get("topics", [])]

	@require_auth
	async def enable_disable_topic(self, topicId: str) -> bool:
		result = await self.req.make_async_request("POST", f"/g/s/rcmd/topics", {
			"topicId": topicId
		})
		data: dict =  await result.json()
		return data["topicEnabled"]

    #referral-code--------------

	@require_auth
	@require_uid
	async def get_my_referral_code(self) -> ReferralCode:
		response = await self.req.make_async_request("GET", f"/g/s/referral-invites/get-invite?uid={self.me.userId}")
		return ReferralCode(await response.json())

	async def get_referral_code_info(self, code: int) -> ReferralCode:
		response = await self.req.make_async_request("GET", f"/g/s/referral-invites/{code}")
		return ReferralCode(await response.json())