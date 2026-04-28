from kyodo.api.base import AsyncBaseClass
from kyodo.utils import require_auth
from kyodo.objects import (
	CircleList,
	ShareLink,
	MediaValue,
	SUPPORTED_MEDIA_FILES,
	MediaTarget,
	AvailableLanguages,
	KyodoObjectTypes,
	ReportTypes,
	Topic,
	AuditLogList,
	NotificationList,
	NoticeList,
	Notice,
	AvatarFrameList,
	ChatBubbleList,
	StoreItems,
	KydoEventsType,
	KyodoEventList
)
from kyodo.utils.exceptions import UnsupportedFileType, UnsupportedArgumentType


from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader
from mimetypes import guess_type


class CommonModule(AsyncBaseClass):

	@require_auth
	async def get_available_languages(self) -> AvailableLanguages:
		response = await self.req.make_async_request("GET", "/g/s/config/available-languages")
		return AvailableLanguages(await response.json())
	
	@require_auth
	async def search(self, query: str | None = None, region: str | None = None, size: int = 10):
		response = await self.req.make_async_request("GET", f"/g/s/circles/search?size={size}&region={region or self.region}{f'&q={query}' if query else ''}")
		return CircleList(await response.json())

	@require_auth
	async def send_active_time(self, circleId: str):
		await self.req.make_async_request("POST", f"/{circleId}/s/live-activity/last-active-time")


	@require_auth
	async def get_link_info(self, link: str) -> ShareLink:
		result = await self.req.make_async_request("POST", f"/g/s/share-links/resolution", {
			"link": link
		})
		return ShareLink(await result.json())

	@require_auth
	async def get_share_link(self, objectId: str, objectType: int, circleId: str | None = None) -> ShareLink:
		result = await self.req.make_async_request("POST", f"/{circleId if circleId else 'g'}/s/share-links", {
			"objectId": objectId,
			"objectType": objectType
		})
		return ShareLink(await result.json())



	@require_auth
	async def upload_media(self, file: IO | BufferedReader | AsyncBufferedReader, target: str = MediaTarget.ChatImageMessage, content_type: str | None = None) -> MediaValue:

		if isinstance(file, (BufferedReader, IO)):
			file_name = file.name
			file_content = file.read()
		elif isinstance(file, AsyncBufferedReader):
			file_name = file.name
			file_content = await file.read()
		else: raise UnsupportedArgumentType(f"file: {type(file)}")

		content_type = content_type if content_type else guess_type(file_name)[0]
		if content_type not in SUPPORTED_MEDIA_FILES: raise UnsupportedFileType(f"file: {content_type}")

		result = await self.req.make_async_request("POST", f"/g/s/media/target/{target}", body=file_content, headers={"Content-Type": content_type})
		return MediaValue(await result.json())


	@require_auth
	async def send_report(self, objectId: str, objectType: int = KyodoObjectTypes.User, reportType: int = ReportTypes.Other, content: str | None = None, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/reports", {
			"objectId": objectId,
			"content": content or "",
			"objectType": objectType,
			"type": reportType
		})
				
	@require_auth
	async def get_topics_list(self, size: int = 25, query: str | None = None) -> list[Topic]:
		response = await self.req.make_async_request("GET", f"/g/s/topics/?size={size}{f'&q={query}' if query else ''}")
		return [Topic(x) for x in (await response.json()).get("topicList", [])]


	@require_auth
	async def get_audit_log(self, objectId: str, objectType: int = KyodoObjectTypes.Chat, circleId: str | None = None, size: int = 20) -> AuditLogList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/audit-logs?size={size}&objectType={objectType}&objectId={objectId}")
		return AuditLogList(await response.json())
	



	@require_auth
	async def get_notices(self, circleId: str, size: int = 25, pageToken: str | None = None) -> NoticeList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/notices?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return NoticeList(await result.json())

	@require_auth
	async def mark_as_read_notice(self, circleId: str | None = None, noticeId: bool = True) -> Notice:
		result = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/notices/{noticeId}/read")
		return Notice((await result.json()).get("notice",{}))


	@require_auth
	async def get_notifications(self, circleId: str | None = None, size: int = 25, pageToken: str | None = None) -> NotificationList:
		result = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/notifications?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return NotificationList(await result.json())
	

	@require_auth
	async def mark_as_read_notifications(self, circleId: str | None = None, markAllRead: bool = True):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/notifications/mark-as-read", {"markAllRead": markAllRead})


	@require_auth
	async def get_store_items(self) -> StoreItems:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/store")
		return StoreItems(await result.json())
	

	@require_auth
	async def get_store_chat_bubbles(self, query: str | None = None, size: int = 25, pageToken: str | None = None) -> ChatBubbleList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/chat-bubbles?type=store-search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return ChatBubbleList(await result.json())

	@require_auth
	async def get_store_latest_chat_bubbles(self, size: int = 25, pageToken: str | None = None) -> ChatBubbleList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/chat-bubbles?type=store-section&parentId=latest-chat-bubbles&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatBubbleList(await result.json())

	@require_auth
	async def get_my_chat_bubbles(self, size: int = 25, pageToken: str | None = None) -> ChatBubbleList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/inventory/chat-bubbles?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatBubbleList(await result.json())



	@require_auth
	async def get_store_avatar_frames(self, query: str | None = None, size: int = 25, pageToken: str | None = None) -> AvatarFrameList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/avatar-frames?type=store-search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return AvatarFrameList(await result.json())


	@require_auth
	async def get_store_latest_avatar_frames(self, size: int = 25, pageToken: str | None = None) -> AvatarFrameList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/avatar-frames?type=store-section&parentId=latest-avatar-frames&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return AvatarFrameList(await result.json())


	@require_auth
	async def get_my_avatar_frames(self, size: int = 25, pageToken: str | None = None) -> AvatarFrameList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/inventory/avatar-frames?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return AvatarFrameList(await result.json())
	


	@require_auth
	async def get_kyodo_events(self, type: str = KydoEventsType.calendar, size: int = 50) -> KyodoEventList:
		result = await self.req.make_async_request("GET", f"/g/s/events?size={size}&type={type}")
		return KyodoEventList(await result.json())