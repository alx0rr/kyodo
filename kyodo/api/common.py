from kyodo.api.base import BaseClass
from kyodo.utils import require_auth
from kyodo.objects import CircleList, ShareLink, MediaValue, SUPPORTED_MEDIA_FILES, MediaTarget
from kyodo.objects import AvailableLanguages, KyodoObjectTypes, ReportTypes, Topic
from kyodo.utils.exceptions import UnsupportedFileType, UnsupportedArgumentType


from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader
from mimetypes import guess_type


class CommonModule(BaseClass):

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