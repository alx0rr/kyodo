from kyodo.api.base import AsyncBaseClass
from kyodo.utils import require_auth
from kyodo.utils.generators import random_ascii_string
from kyodo import exceptions
from kyodo.objects import (
	Circle, 
	CircleInfo,
	MediaTarget,
	CircleTemplate,
	CirclePrivacy,
	ExploreModule,
	JoinRequestList,
	UserProfile,
	MuteDuration,
	UserTitle,
	UserProfileList,
	CircleAlerts,
	CircleInviteLink,
	CircleAdminStats,
	AuditLogList,
	ChatsList,
	PostList,
	ChatRoomPermission,
	WikiPermission,
	ArticlePermission,
	ThreadsPermission,
	CircleUsersStaffType,
	CircleRole,
	Topic,
	CirclePageType,
	FeaturedLayoutTypes,
	CircleListingTasks,
	CircleReportList,
	UserAlerts
)
from kyodo.utils.generators import strtime

from aiofiles.threadpool.binary import AsyncBufferedReader
from typing import IO
from _io import BufferedReader


class CircleModule(AsyncBaseClass):

	@require_auth
	async def get_joined_circles(self) -> list[Circle]:
		response = await self.req.make_async_request("GET", "/g/s/circles/joined")
		return [Circle(x) for x in (await response.json()).get("circleList")]

	@require_auth
	async def get_unread_circleIds(self) -> list[str]:
		response = await self.req.make_async_request("GET", "/g/s/notifications/unread-circle-ids")
		return (await response.json()).get("circleIdList", [])


	@require_auth
	async def get_circle_info(self, circleId: str) -> CircleInfo:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles")
		return CircleInfo(await response.json())
		
	@require_auth
	async def get_circle_description(self, circleId: str) -> str:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/description")
		return (await response.json()).get("description", '')
	
	@require_auth
	async def get_circle_guidelines(self, circleId: str) -> str:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/guidelines")
		return (await response.json()).get("guidelines", '')


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



	@require_auth
	async def get_7d_leaderboard(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/leaderboard/ranking?type=active-7d&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	

	@require_auth
	async def get_24h_leaderboard(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/leaderboard/ranking?type=active-24h&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())



	@require_auth
	async def get_circle_alerts(self, circleId: str) -> CircleAlerts:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/alerts/check")
		return CircleAlerts(await response.json())




class CircleAdminModule(AsyncBaseClass):

	async def _build_mediamap(self, mediaMap: list[dict[str, IO | BufferedReader | AsyncBufferedReader]],
			target: MediaTarget, content: str) -> tuple[dict, str]:
		result = {}
		for x in mediaMap:
			key, value = next(iter(x.items()))
			mediaId = random_ascii_string(10, True)
			result[mediaId] = {
				"src": (await self.upload_media(value, target)).url,
				"isCover": False,
				"type": 0
			}
			content = content.replace(
				f"![{key}]", f"![{mediaId}](mediamap://{mediaId})"
			)
		return result, content

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
	async def delete_circle(self, circleId: str, password: str) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/delete", {
			"secret": password,
		})

		return Circle((await response.json()).get("circle", {}))






	@require_auth
	async def get_reports_count(self, circleId: str) -> int:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/reports/pending-count")

		return (await response.json()).get("reportCount", 0)
	

	@require_auth
	async def get_join_requests_count(self, circleId: str) -> int:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/admin/join-requests/count")
		return (await response.json()).get("membersPendingCount", 0)

	@require_auth
	async def get_posts_count(self, circleId: str) -> int:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts/count")
		return (await response.json()).get("postCount", 0)


	@require_auth
	async def check_alerts(self, circleId: str) -> UserAlerts:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/alerts/check")
		return UserAlerts(await response.json())
	

	@require_auth
	async def edit_circle_privacy(self, circleId: str, joinPermission: int = CirclePrivacy.Open) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"privacy": joinPermission
		})
		return Circle((await response.json()).get("circle", {}))
	
	@require_auth
	async def create_invite_link(self, circleId: str) -> CircleInviteLink:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/invites")
		return CircleInviteLink((await response.json()).get("invite", {}))

	@require_auth
	async def delete_invite_link(self, circleId: str):
		await self.req.make_async_request("POST", f"/{circleId}/s/circles/invites/delete")
	

	@require_auth
	async def edit_circle_vanity(self, circleId: str, vanity: str) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/vanity", {
			"vanity": vanity
		})
		return Circle((await response.json()).get("circle", {}))
	
	@require_auth
	async def check_circle_listing_tasks(self, circleId: str) -> CircleListingTasks:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/admin/listing/tasks")
		return CircleListingTasks(await response.json())
	
	@require_auth
	async def check_circle_stats(self, circleId: str) -> CircleAdminStats:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/admin/stats")
		return CircleAdminStats(await response.json())
	
	@require_auth
	async def get_circle_reports(self, circleId: str, size: str = 25, pageToken: str | None = None) -> CircleReportList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/reports?type=pending&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return CircleReportList(await response.json())
	
	@require_auth
	async def get_circle_audit_logs(self, circleId: str, size: str = 25, pageToken: str | None = None) -> AuditLogList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/audit-logs?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return AuditLogList(await response.json())
	
	@require_auth
	async def get_search_chats(self, circleId: str, size: int = 25, pageToken: str | None = None, query: str | None = None) -> ChatsList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/chats?type=search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return ChatsList(await response.json())

	@require_auth
	async def get_search_circle_posts(self, circleId: str, size: int = 25, pageToken: str | None = None, query: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return PostList(await response.json())

	@require_auth
	async def get_search_users(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type=search&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())


	@require_auth
	async def get_banned_users(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type=banned&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())

	@require_auth
	async def get_staff_users(self, circleId: str, type: str = CircleUsersStaffType.Invited, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type={type}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())

	@require_auth
	async def edit_circle_chats_permission(self, circleId: str, chatRoomPermission: int = ChatRoomPermission.Anyone) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"chatRoomPermission": chatRoomPermission
		})
		return Circle((await response.json()).get("circle", {}))

	@require_auth
	async def edit_circle_article_permission(self, circleId: str, articlePermission: int = ArticlePermission.Anyone) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"articlePermission": articlePermission
		})
		return Circle((await response.json()).get("circle", {}))

	@require_auth
	async def edit_circle_threads_ermission(self, circleId: str, threadsPermission: int = ThreadsPermission.Anyone) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"threadsPermission": threadsPermission
		})
		return Circle((await response.json()).get("circle", {}))

	@require_auth
	async def edit_circle_wiki_permission(self, circleId: str, wikiPermission: int = WikiPermission.Anyone) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"wikiPermission": wikiPermission
		})
		return Circle((await response.json()).get("circle", {}))


	@require_auth
	async def promote_to_circle_staff(self, circleId: str, userId: str, role: int = CircleRole.Moderator):
		await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/admin/promote", {
			"role": role
		})


	@require_auth
	async def cancel_promote_to_circle_staff(self, circleId: str, userId: str):
		await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/role-invites/{userId}/cancel")

	@require_auth
	async def edit_circle(self, circleId: str, iconUrl: str, coverUrl: str, name: str, tagline: str, themeHexColor: str, isThemeDark: bool) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"iconUrl": iconUrl,
			"coverUrl": coverUrl,
			"name": name,
			"tagline": tagline,
			"themeColor": themeHexColor,
			"isThemeDark": isThemeDark
		})
		return Circle((await response.json()).get("circle", {}))
	
	@require_auth
	async def edit_circle_guideline(self, circleId: str, guidelines: str = "") -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"guidelines": guidelines
		})
		return Circle((await response.json()).get("circle", {}))
	
	@require_auth
	async def edit_circle_description(self, circleId: str, content: str = "", mediaMap: list[dict[str, IO | BufferedReader]] | None = None) -> Circle:
		payload = {
			"mediaMap": {}
		}

		if mediaMap:
			payload["mediaMap"], content = await self._build_mediamap(
				mediaMap, MediaTarget.CircleIcon, content
			)
		payload["content"] = content

		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/edit", payload)
		return Circle((await response.json()).get("circle", {}))

	@require_auth
	async def get_circle_topics_list(self, circleId: str, size: int = 25, query: str | None = None) -> list[Topic]:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/topics/?size={size}{f'&q={query}' if query else ''}")
		return [Topic(x) for x in (await response.json()).get("topicList", [])]
	
	@require_auth
	async def edit_circle_topics(self, circleId: str, topicIds: list[str]) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"topicIds": topicIds
		})
		return Circle((await response.json()).get("circle", {}))

	@require_auth
	async def edit_circle_sidebar_image(self, circleId: str, image: IO | BufferedReader) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"sidebarCoverUrl": (await self.upload_media(image, MediaTarget.CircleSidebar)).url
		})
		return Circle((await response.json()).get("circle", {}))

	@require_auth
	async def reorder_circle_pages(self, circleId: str, pageIds: list[str]) -> Circle:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize/home-layout/pages/reorder", {
			"pageIds": pageIds
		})
		return Circle((await response.json()).get("circle", {}))


	@require_auth
	async def delete_circle_page(self, circleId: str, pageId: str) -> Circle:
		response = await self.req.make_async_request("DELETE", f"/{circleId}/s/circles/admin/customize/home-layout/pages/{pageId}")
		return Circle((await response.json()).get("circle", {}))


	@require_auth
	async def edit_circle_page(self, circleId: str, pageId: str, label: str, featuredLayout: int, content: str, pageType: str, isStartPage: bool = False) -> Circle:

		match pageType:
			case CirclePageType.WebPage:
				if not content:
					raise exceptions.ArgumentNeeded("For this page format, you must specify a link to the resource in the content argument")
			case CirclePageType.Post:
				if not content:
					raise exceptions.ArgumentNeeded("This page format requires you to specify a link to the post in the circle in the content argument")

		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize/home-layout/pages/{pageId}", {
			"id": pageId,
			"page": pageType,
			"label": label,
			"content": content,
			"featuredLayout": featuredLayout,
			"isStartPage": isStartPage
		})
		return Circle((await response.json()).get("circle", {}))


	@require_auth
	async def create_circle_page(self, circleId: str, label: str, featuredLayout: int = FeaturedLayoutTypes.Compact, content: str = "", pageType: str = CirclePageType.Guidlines, isStartPage: bool = False) -> Circle:

		match pageType:
			case CirclePageType.WebPage:
				if not content:
					raise exceptions.ArgumentNeeded("For this page format, you must specify a link to the resource in the content argument")
			case CirclePageType.Post:
				if not content:
					raise exceptions.ArgumentNeeded("This page format requires you to specify a link to the post in the circle in the content argument")


		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/admin/customize/home-layout/pages", {
			"id": f"np-{strtime()}",
			"page": pageType,
			"label": label,
			"content": content,
			"featuredLayout": featuredLayout,
			"isStartPage": isStartPage
		})
		return Circle((await response.json()).get("circle", {}))