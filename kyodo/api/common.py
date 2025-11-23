
from .base import BaseClass
from ..objects import (
	MediaTarget, MediaValue, SUPPORTED_MEDIA_FILES,
    OperationLogs, HealthServices, HandleInfo, ShareLink,
	HomefeedExplore, NoticesList, NotificationsList, PostsList,
	Notice, CirclesList, FeedsList, BroadcastsList
	
)
from ..utils import require_auth, exceptions
from ..utils.generators import get_utc_time

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader
from mimetypes import guess_type




class CommonModule(BaseClass):

	@require_auth
	async def get_link_info(self, link: str) -> ShareLink:
		code = link.split("/")[-1]
		result = await self.req.make_async_request("GET", 
			f"/g/s/circles/vanities/{code}" if "s/c/" in link else f"/g/s/share-links/{code}"
		)
		return ShareLink(await result.json())

	@require_auth
	async def get_share_link(self, objectId: str, objectType: int, circleId: str | None = None) -> ShareLink:
		result = await self.req.make_async_request("POST", f"/{circleId if circleId else 'g'}/s/share-links/", {
			"contentId": objectId,
			"contentType": objectType
		})
		return ShareLink(await result.json())

	@require_auth
	async def get_operation_logs(self, circleId: str, objectId: str, objectType: int, limit: int = 3, start: int = 0) -> OperationLogs:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/circles/operation-logs?objectType={objectType}&objectId={objectId}&limit={limit}&start={start}")
		return OperationLogs(await result.json())

	@require_auth
	async def broadcast_page(self, text: str, circleId: str, objectId: str, objectType: int) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/push-track", {
			"content": text,
			"objectType": objectType,
			"objectId": objectId,
			"targetTime": get_utc_time()
		})
		return True


	@require_auth
	async def get_broadcast_history(self, circleId: str, start: int = 0, limit: int = 20) -> BroadcastsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/push-track?limit={limit}&start={start}")
		return BroadcastsList(await result.json())


	@require_auth
	async def report(self, text: str, circleId: str, objectId: str, objectType: int, reportType: int) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/reports/content", {
			"contentId": objectId,
			"contentType": objectType,
			"reason": text,
			"type": reportType
		})
		return True

	@require_auth
	async def upload_media(self, file: IO | BufferedReader | AsyncBufferedReader, target: str = MediaTarget.ChatImageMessage) -> MediaValue:
		raise NotImplementedError(
			"The current version of the library does not support loading media files. Please update to the latest version or suggest a fix for this feature on GitHub. https://github.com/xXxCLOTIxXx/kyodo"
		)
		if isinstance(file, (BufferedReader, IO)):
			file_name = file.name
			file_content = file.read()
		elif isinstance(file, AsyncBufferedReader):
			file_name = file.name
			file_content = await file.read()
		else: raise exceptions.UnsupportedArgumentType(f"file: {type(file)}")

		content_type = guess_type(file_name)[0]
		if content_type not in SUPPORTED_MEDIA_FILES: raise exceptions.UnsupportedFileType(f"file: {content_type}")

		result = await self.req.make_async_request("POST", f"/g/s/media/target/{target}", body=file_content, headers={"Content-Type": content_type})
		return MediaValue(await result.json())

	async def get_system_account(self) -> HandleInfo:
		return await self.check_username_in_use("system")

	async def get_health_services(self) -> HealthServices:
		result = await self.req.make_async_request("GET", f"/g/s/health/services")
		data: dict = await result.json()
		return HealthServices(data["healthChecks"])

	async def get_supported_languages(self) -> list[str]:
		response = await self.req.make_async_request("GET", f"/g/s/announcements/languages")
		data: dict = await response.json()
		return data["languages"]
	
	@require_auth
	async def get_homefeed_explore(self, showNsfw: bool = False) -> HomefeedExplore:
		response = await self.req.make_async_request("GET", f"/g/s/homefeed/discovery/explore?showNsfw={showNsfw}")
		return HomefeedExplore(await response.json())
	
	@require_auth
	async def get_homefeed_joined_circles(self, start: int = 0, limit: int = 20) -> CirclesList:
		response = await self.req.make_async_request("GET", f"/g/s/homefeed/joined?start={start}&limit={limit}")
		return CirclesList(await response.json())

	@require_auth
	async def get_homefeed_personal(self, start: int = 0, limit: int = 20) -> FeedsList:
		response = await self.req.make_async_request("GET", f"/g/s/homefeed/personal?start={start}&limit={limit}")
		return FeedsList(await response.json())

	@require_auth
	async def get_notices(self, start: int = 0, limit: int = 3, showAll: bool = False, getAllJoined: bool = True) -> NoticesList:
		response = await self.req.make_async_request("GET", f"/g/s/notices?limit={limit}&start={start}&showAll={showAll}&getAllJoined={getAllJoined}")
		return NoticesList(await response.json())

	@require_auth
	async def get_notice(self, noticeId: str) -> bool:
		response = await self.req.make_async_request("GET", f"/g/s/notices/{noticeId}")
		data: dict = await response.json()
		return Notice(data["notice"])

	@require_auth
	async def get_notifications(self, start: int = 0, limit: int = 3) -> NotificationsList:
		response = await self.req.make_async_request("GET", f"/g/s/notifications?limit={limit}&start={start}")
		return NotificationsList(await response.json())

	@require_auth
	async def get_announcements(self, start: int = 0, limit: int = 15) -> PostsList:
		response =  await self.req.make_async_request("GET", f"/g/s/posts?type=7&limit={limit}&start={start}")
		return PostsList(await response.json())

	@require_auth
	async def mark_as_read_notifications(self) -> bool:
		await self.req.make_async_request("POST", f"/g/s/notifications/read")
		return True


	@require_auth
	async def mark_as_read_notice(self, noticeId: str) -> bool:
		await self.req.make_async_request("POST", f"/g/s/notices/{noticeId}/read")
		return True

	@require_auth
	async def mark_as_read_announcements(self) -> bool:
		await self.req.make_async_request("POST", f"/g/s/announcements/read")
		return True

	@require_auth
	async def get_announcements_unread_count(self) -> int:
		response =  await self.req.make_async_request("GET", f"/g/s/announcements/unread-count")
		data: dict = await response.json()
		return data["count"]