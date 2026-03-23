from kyodo.api.base import BaseClass
from kyodo.utils import require_auth
from kyodo.objects import Circle, CircleInfo, MediaTarget, CircleTemplate, CirclePrivacy, ExploreModule, JoinRequestList, UserProfile, MuteDuration, UserTitle, UserProfileList
from kyodo.utils.generators import strtime

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
	async def request_to_join_circle(self, circleId: str, message: str):
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




class CircleAdminModule(BaseClass):


	@require_auth
	async def get_circle_join_requests(self, circleId: str, size: str = 25, pageToken: str | None = None) -> JoinRequestList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/admin/join-requests?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return JoinRequestList(await response.json())
	

	@require_auth
	async def resolve_circle_join_request(self, circleId: str, userId: str, isApproved: bool = True):
		await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/join-requests/{userId}/resolve", {
			"isApproved": isApproved
		})
	
	@require_auth
	async def hide_user(self, circleId: str, userId: str, note: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/hide", {
			"note": note or ''
		})
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def unhide_user(self, circleId: str, userId: str, note: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/unhide", {
			"note": note or ''
		})
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def strike_user(self, circleId: str, userId: str, message: str, muteTime: str = MuteDuration.ONE_HOUR):
		await self.req.make_async_request("POST", f"/{circleId}/s/notices", {
			"uid": userId,
			"content": message,
			"time": muteTime
		})


	@require_auth
	async def revoke_strike_user(self, circleId: str, userId: str, note: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/revoke-strike", {
			"note": note or ''
		})
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def warn_user(self, circleId: str, userId: str, message: str):
		await self.req.make_async_request("POST", f"/{circleId}/s/notices", {
			"uid": userId,
			"content": message,
		})


	@require_auth
	async def ban_user(self, circleId: str, userId: str, message: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/ban", {
			"note": message or ''
		})
		return UserProfile((await response.json()).get("userProfile", {}))


	@require_auth
	async def unban_user(self, circleId: str, userId: str, message: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/unban", {
			"note": message or ''
		})
		return UserProfile((await response.json()).get("userProfile", {}))
	



	@require_auth
	async def edit_user_titles(
		self,
		circleId: str,
		userId: str,
		titles: list[dict | UserTitle]
	) -> UserProfile:

		title_list = []


		for x in titles:
			if isinstance(x, UserTitle):
				title = {
					"id": x.id or strtime(),
					"text": x.text,
					"bg": x.bg,
					"fg": x.fg,
				}

				if x.isOfficial is not None:
					title["isOfficial"] = x.isOfficial

				title_list.append(title)

			elif isinstance(x, dict):
				title = {
					"id": x.get("id") or strtime(),
					"text": x.get("text"),
					"bg": x.get("bg"),
					"fg": x.get("fg"),
				}

				if "isOfficial" in x and x.get("isOfficial") is not None:
					title["isOfficial"] = x.get("isOfficial")

				title_list.append(title)

		response = await self.req.make_async_request(
			"POST",
			f"/{circleId}/s/users/{userId}/titles",
			{"titleList": title_list}
		)

		data = await response.json()
		return UserProfile(data.get("userProfile", {}))
	



	@require_auth
	async def get_7d_leaderboard(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/leaderboard/ranking?type=active-7d&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	

	@require_auth
	async def get_24h_leaderboard(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/leaderboard/ranking?type=active-24h&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())