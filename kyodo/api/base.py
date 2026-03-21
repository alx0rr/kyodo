from kyodo import (
	AccountInfo, UserProfile, MediaTarget, MediaValue
)

from ..utils.requester import Requester
from ..ws import Socket


from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader


class BaseClass(Socket):
	account: AccountInfo = AccountInfo({})
	me: UserProfile = UserProfile({})
	req: Requester
	socket_enable: bool
	error_trace: bool

	@property
	def language(self) -> str:
		return self.req.language
	
	@property
	def region(self) -> str:
		return self.req.region

	@property
	def user_agent(self) -> str:
		return self.req.user_agent

	@property
	def timezone(self) -> str:
		return self.req.timezone

	@property
	def token(self) -> str:
		return self.req.token

	@property
	def deviceId(self) -> str:
		return self.req.deviceId

	@property
	def userId(self) -> str | None:
		return self.account.userId

	async def upload_media(self, file: IO | BufferedReader | AsyncBufferedReader, target: str = MediaTarget.ChatImageMessage, content_type: str | None = None) -> MediaValue: ...

