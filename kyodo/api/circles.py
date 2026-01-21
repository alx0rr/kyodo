from .base import BaseClass
from ..objects import (
	MediaTarget, Circle, CircleInfo, MeetMatch, CircleRole,
	CirclesList, ReportsList, CircleStats, Topic, CircleDiscoveryRequirements
)
from ..utils import require_auth
from .. import exceptions

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader




class CirclesModule(BaseClass):

	async def search_circles(self, name: str | None = None, start: int = 0, limit: int = 15, showNsfw: bool = False) -> CirclesList:
		result = await self.req.make_async_request("GET", f"/g/s/circles/search?limit={limit}&start={start}&showNsfw={showNsfw}&q={name or ''}")
		return CirclesList(await result.json())

	@require_auth
	async def join_circle(self, circleId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/circles/join")
		return True

	@require_auth
	async def leave_circle(self, circleId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/circles/leave")
		return True

	@require_auth
	async def create_circle(self, name: str, icon: IO | BufferedReader | AsyncBufferedReader, language: str | None = None, with_language_fallback: bool = True) -> Circle:
		icon_data = await self.upload_media(icon, MediaTarget.CircleIcon)

		result = await self.req.make_async_request("POST", f"/g/s/circles", {
			"name": name,
			"icon": icon_data.url,
			"language": language or self.language,
			"withLanguageFallback": with_language_fallback
		})

		return Circle(await result.json())


	@require_auth
	async def get_my_circles(self) -> list[str]:
		result = await self.req.make_async_request("GET", f"/g/s/accounts/joined-circles")
		data: dict = await result.json()
		return data["circleIds"]


	@require_auth
	async def get_unread_circles(self) -> list[str]:
		result = await self.req.make_async_request("GET", f"/g/s/circles/unread")
		data: dict = await result.json()
		return data["circleIds"]

	@require_auth
	async def get_circle_info(self, circleId: str) -> CircleInfo:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/circles")
		return CircleInfo(await result.json())


	#meet---------------------

	@require_auth
	async def set_up_meetings(self, circleId: str, text: str) -> MeetMatch:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/meet/match", {
			"content": text
		})
		data: dict = await result.json()
		return MeetMatch(data.get("match", {}))

	@require_auth
	async def fetch_meetings(self, circleId: str) -> MeetMatch | None:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/meet/pool/fetch")
		data: dict = await result.json()
		return MeetMatch(data.get("match")) if data.get("match") else None

	@require_auth
	async def accept_meeting(self, circleId: str, matchId: str) -> str:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/meet/match/{matchId}/accept")
		data: dict = await result.json()
		return data["chatId"]

	@require_auth
	async def reject_meeting(self, circleId: str, matchId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/meet/match/{matchId}/reject")
		return True
	


	#adm----------------


	@require_auth
	async def circle_report_count(self, circleId: str) -> int:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/circles/report-queue/pending-count")
		data: dict = await result.json()
		return data["reportCount"]

	@require_auth
	async def get_circle_reports(self, circleId: str, start: int = 0, limit: int = 15) -> ReportsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/circles/report-queue?limit={limit}&start={start}")
		return ReportsList(await result.json())

	@require_auth
	async def change_circle_vanity(self, circleId: str, vanity: str) -> bool:
		await self.req.make_async_request("PUT", f"/{circleId}/s/circles/vanity", {
			"vanity": vanity
		})
		return True

		

	@require_auth
	async def edit_circle(self, circleId: str, language: str | None = None, name: str | None = None, guidelines: str | None = None, postsModule: int | None = None,
		chatsModule: int | None = None, joinInviteOnly: bool | None = None,
		enablePersons: bool | None = None, icon: IO | BufferedReader | AsyncBufferedReader | None = None, banner: IO | BufferedReader | AsyncBufferedReader | None = None) -> Circle:
		
		data = {}
		module_types = {}
		if icon:
			icon_data = await self.upload_media(icon, MediaTarget.CircleIcon)
			data["icon"]=icon_data.url
		if banner:
			banner_data = await self.upload_media(banner, MediaTarget.UserBanner)
			data["banner"]=banner_data.url
		if language:
			data["language"]=language
		if name:
			data["name"]=name
		if guidelines:
			data["guidelines"]=guidelines
		
		if enablePersons is not None:
			data["ocModuleEnabled"]=enablePersons
		if joinInviteOnly is not None:
			data["privacy"]= 0 if joinInviteOnly else 1
		if postsModule:
			module_types["posts"]=postsModule
		if chatsModule:
			module_types["chats"]=chatsModule

		if module_types:data["moduleTypes"] = module_types

		if not data:raise exceptions.NoDataError
		result = await self.req.make_async_request("PUT", f"/{circleId}/s/circles", data)
		data: dict = await result.json()
		return Circle(data["circle"])


	@require_auth
	async def delete_circle(self, circleId: str) -> bool:
		await self.req.make_async_request("DELETE", f"/{circleId}/s/circles")
		return True


	@require_auth
	async def transfer_circle_owner(self, circleId: str, userId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/users/role-invite", {
			"uid": userId,"role": CircleRole.Owner
		})

		return True

	@require_auth
	async def circle_admin_invite(self, circleId: str, userId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/users/role-invite", {
			"uid": userId,"role": CircleRole.Admin
		})
		return True

	@require_auth
	async def circle_moderator_invite(self, circleId: str, userId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/users/role-invite", {
			"uid": userId,"role": CircleRole.Moderator
		})
		return True


	@require_auth
	async def get_circle_stats(self, circleId: str) -> CircleStats:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/circles/stats")
		data: dict = await result.json()
		return CircleStats(data["stats"])
	
	@require_auth
	async def set_circle_topic(self, circleId: str, topicId: str) -> Topic:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/circles/discovery/topics/primary", {
			"topicId": topicId
		})
		data: dict = await result.json()
		return Topic(data["topic"])
	
	@require_auth
	async def get_circle_discovery_requirements(self, circleId: str) -> CircleDiscoveryRequirements:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/circles/discovery/requirements")
		data: dict = await result.json()
		return CircleDiscoveryRequirements(data["requirements"])