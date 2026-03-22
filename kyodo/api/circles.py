from kyodo.api.base import BaseClass
from kyodo.utils import require_auth
from kyodo.objects import Circle, CircleInfo, MediaTarget, CircleTemplate, CirclePrivacy, ExploreModule

from aiofiles.threadpool.binary import AsyncBufferedReader
from typing import IO
from _io import BufferedReader

class CircleModule(BaseClass):

	@require_auth
	async def get_joined_circles(self) -> list[Circle]:
		response = await self.req.make_async_request("GET", "/g/s/circles/joined")
		return [Circle(x) for x in (await response.json()).get("circleList")]
		

	@require_auth
	async def get_circle_info(self, circleId: str) -> CircleInfo:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles")
		return CircleInfo(await response.json())
		
	@require_auth
	async def get_circle_description(self, circleId: str) -> str:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/description")
		return (await response.json()).get("description", '')
	
	@require_auth
	async def join_circle(self, circleId: str, invitationId: str | None = None) -> CircleInfo:
		payload = {}
		if invitationId: payload["invitationId"] = invitationId
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/join", payload)
		return CircleInfo(await response.json())

	@require_auth
	async def request_to_join_circle_(self, circleId: str, message: str):
		await self.req.make_async_request("POST", f"/{circleId}/s/circles/request-to-join", {"content": message})


	@require_auth
	async def leave_circle(self, circleId: str) -> CircleInfo:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/leave")
		return CircleInfo(await response.json())
	
	@require_auth
	async def create_circle(
		self, name: str, image: IO | BufferedReader | AsyncBufferedReader, themeColor: str = "#0090FF", isThemeDark: bool = True,
		language: str = "en", privacy: int = CirclePrivacy.Open, templateId: int = CircleTemplate.FromScratch
	) -> CircleInfo:
		
		url = (await self.upload_media(image, MediaTarget.CircleIcon)).url
		response = await self.req.make_async_request("POST", f"/g/s/circles", {
			"iconUrl": url,
			"name": name,
			"themeColor": themeColor,
			"isThemeDark": isThemeDark,
			"language": language,
			"privacy": privacy,
			"templateId": templateId
		})
		return CircleInfo(await response.json())
	



	@require_auth
	async def get_explore_page(self, region: str | None = None) -> list[ExploreModule]:
		response = await self.req.make_async_request("GET", f"/g/s/explore/?region={region or self.region}")
		return [ExploreModule(x) for x in (await response.json()).get("exploreModuleList", [])]

	@require_auth
	async def get_explore_suggested_page(self) -> list[Circle]:
		response = await self.req.make_async_request("GET", f"/g/s/explore/suggested")
		return [Circle(x) for x in (await response.json()).get("circleList", [])]