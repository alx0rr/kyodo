from kyodo.api.base import SyncBaseClass
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
from mimetypes import guess_type


class CommonModule(SyncBaseClass):

	@require_auth
	def get_available_languages(self) -> AvailableLanguages:
		response = self.req.make_request("GET", "/g/s/config/available-languages")
		return AvailableLanguages(response.json())
	
	@require_auth
	def search(self, query: str | None = None, region: str | None = None, size: int = 10):
		response = self.req.make_request("GET", f"/g/s/circles/search?size={size}&region={region or self.region}{f'&q={query}' if query else ''}")
		return CircleList(response.json())

	@require_auth
	def send_active_time(self, circleId: str):
		self.req.make_request("POST", f"/{circleId}/s/live-activity/last-active-time")


	@require_auth
	def get_link_info(self, link: str) -> ShareLink:
		result = self.req.make_request("POST", f"/g/s/share-links/resolution", {
			"link": link
		})
		return ShareLink(result.json())

	@require_auth
	def get_share_link(self, objectId: str, objectType: int, circleId: str | None = None) -> ShareLink:
		result = self.req.make_request("POST", f"/{circleId if circleId else 'g'}/s/share-links", {
			"objectId": objectId,
			"objectType": objectType
		})
		return ShareLink(result.json())



	@require_auth
	def upload_media(self, file: IO | BufferedReader, target: str = MediaTarget.ChatImageMessage, content_type: str | None = None) -> MediaValue:

		if isinstance(file, (BufferedReader, IO)):
			file_name = file.name
			file_content = file.read()
		else: raise UnsupportedArgumentType(f"file: {type(file)}")

		content_type = content_type if content_type else guess_type(file_name)[0]
		if content_type not in SUPPORTED_MEDIA_FILES: raise UnsupportedFileType(f"file: {content_type}")

		result = self.req.make_request("POST", f"/g/s/media/target/{target}", body=file_content, headers={"Content-Type": content_type})
		return MediaValue(result.json())


	@require_auth
	def send_report(self, objectId: str, objectType: int = KyodoObjectTypes.User, reportType: int = ReportTypes.Other, content: str | None = None, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/reports", {
			"objectId": objectId,
			"content": content or "",
			"objectType": objectType,
			"type": reportType
		})
				
	@require_auth
	def get_topics_list(self, size: int = 25, query: str | None = None) -> list[Topic]:
		response = self.req.make_request("GET", f"/g/s/topics/?size={size}{f'&q={query}' if query else ''}")
		return [Topic(x) for x in (response.json()).get("topicList", [])]


	@require_auth
	def get_audit_log(self, objectId: str, objectType: int = KyodoObjectTypes.Chat, circleId: str | None = None, size: int = 20) -> AuditLogList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/audit-logs?size={size}&objectType={objectType}&objectId={objectId}")
		return AuditLogList(response.json())
	



	@require_auth
	def get_notices(self, circleId: str, size: int = 25, pageToken: str | None = None) -> NoticeList:
		result = self.req.make_request("GET", f"/{circleId}/s/notices?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return NoticeList(result.json())

	@require_auth
	def mark_as_read_notice(self, circleId: str | None = None, noticeId: bool = True) -> Notice:
		result = self.req.make_request("POST", f"/{circleId or 'g'}/s/notices/{noticeId}/read")
		return Notice((result.json()).get("notice",{}))


	@require_auth
	def get_notifications(self, circleId: str | None = None, size: int = 25, pageToken: str | None = None) -> NotificationList:
		result = self.req.make_request("GET", f"/{circleId or 'g'}/s/notifications?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return NotificationList(result.json())
	

	@require_auth
	def mark_as_read_notifications(self, circleId: str | None = None, markAllRead: bool = True):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/notifications/mark-as-read", {"markAllRead": markAllRead})


	@require_auth
	def get_store_items(self) -> StoreItems:
		result = self.req.make_request("GET", f"/g/s/monetization/store")
		return StoreItems(result.json())
	

	@require_auth
	def get_store_chat_bubbles(self, query: str | None = None, size: int = 25, pageToken: str | None = None) -> ChatBubbleList:
		result = self.req.make_request("GET", f"/g/s/monetization/chat-bubbles?type=store-search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return ChatBubbleList(result.json())

	@require_auth
	def get_store_latest_chat_bubbles(self, size: int = 25, pageToken: str | None = None) -> ChatBubbleList:
		result = self.req.make_request("GET", f"/g/s/monetization/chat-bubbles?type=store-section&parentId=latest-chat-bubbles&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatBubbleList(result.json())

	@require_auth
	def get_my_chat_bubbles(self, size: int = 25, pageToken: str | None = None) -> ChatBubbleList:
		result = self.req.make_request("GET", f"/g/s/monetization/inventory/chat-bubbles?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatBubbleList(result.json())



	@require_auth
	def get_store_avatar_frames(self, query: str | None = None, size: int = 25, pageToken: str | None = None) -> AvatarFrameList:
		result = self.req.make_request("GET", f"/g/s/monetization/avatar-frames?type=store-search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return AvatarFrameList(result.json())


	@require_auth
	def get_store_latest_avatar_frames(self, size: int = 25, pageToken: str | None = None) -> AvatarFrameList:
		result = self.req.make_request("GET", f"/g/s/monetization/avatar-frames?type=store-section&parentId=latest-avatar-frames&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return AvatarFrameList(result.json())


	@require_auth
	def get_my_avatar_frames(self, size: int = 25, pageToken: str | None = None) -> AvatarFrameList:
		result = self.req.make_request("GET", f"/g/s/monetization/inventory/avatar-frames?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return AvatarFrameList(result.json())
	


	@require_auth
	def get_kyodo_events(self, type: str = KydoEventsType.calendar, size: int = 50) -> KyodoEventList:
		result = self.req.make_request("GET", f"/g/s/events?size={size}&type={type}")
		return KyodoEventList(result.json())