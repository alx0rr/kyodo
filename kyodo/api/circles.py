from kyodo.api.base import SyncBaseClass
from kyodo.utils import require_auth
from kyodo import exceptions
from kyodo.utils.generators import random_ascii_string
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

from typing import IO
from _io import BufferedReader


class CircleModule(SyncBaseClass):

	@require_auth
	def get_joined_circles(self) -> list[Circle]:
		response = self.req.make_request("GET", "/g/s/circles/joined")
		return [Circle(x) for x in (response.json()).get("circleList")]

	@require_auth
	def get_unread_circleIds(self) -> list[str]:
		response = self.req.make_request("GET", "/g/s/notifications/unread-circle-ids")
		return (response.json()).get("circleIdList", [])


	@require_auth
	def get_circle_info(self, circleId: str) -> CircleInfo:
		response = self.req.make_request("GET", f"/{circleId}/s/circles")
		return CircleInfo(response.json())
		
	@require_auth
	def get_circle_description(self, circleId: str) -> str:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/description")
		return (response.json()).get("description", '')
	
	@require_auth
	def get_circle_guidelines(self, circleId: str) -> str:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/guidelines")
		return (response.json()).get("guidelines", '')


	@require_auth
	def join_circle(self, circleId: str, invitationId: str | None = None) -> CircleInfo:
		payload = {}
		if invitationId: payload["invitationId"] = invitationId
		response = self.req.make_request("POST", f"/{circleId}/s/circles/join", payload)
		return CircleInfo(response.json())

	@require_auth
	def request_to_join_circle(self, circleId: str, message: str):
		self.req.make_request("POST", f"/{circleId}/s/circles/request-to-join", {"content": message})


	@require_auth
	def leave_circle(self, circleId: str) -> CircleInfo:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/leave")
		return CircleInfo(response.json())
	
	@require_auth
	def create_circle(
		self, name: str, image: IO | BufferedReader, themeColor: str = "#0090FF", isThemeDark: bool = True,
		language: str = "en", privacy: int = CirclePrivacy.Open, templateId: int = CircleTemplate.FromScratch
	) -> CircleInfo:
		
		url = (self.upload_media(image, MediaTarget.CircleIcon)).url
		response = self.req.make_request("POST", f"/g/s/circles", {
			"iconUrl": url,
			"name": name,
			"themeColor": themeColor,
			"isThemeDark": isThemeDark,
			"language": language,
			"privacy": privacy,
			"templateId": templateId
		})
		return CircleInfo(response.json())
	



	@require_auth
	def get_explore_page(self, region: str | None = None) -> list[ExploreModule]:
		response = self.req.make_request("GET", f"/g/s/explore/?region={region or self.region}")
		return [ExploreModule(x) for x in (response.json()).get("exploreModuleList", [])]

	@require_auth
	def get_explore_suggested_page(self) -> list[Circle]:
		response = self.req.make_request("GET", f"/g/s/explore/suggested")
		return [Circle(x) for x in (response.json()).get("circleList", [])]



	@require_auth
	def get_7d_leaderboard(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/leaderboard/ranking?type=active-7d&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())
	

	@require_auth
	def get_24h_leaderboard(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/leaderboard/ranking?type=active-24h&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())



	@require_auth
	def get_circle_alerts(self, circleId: str) -> CircleAlerts:
		response = self.req.make_request("GET", f"/{circleId}/s/alerts/check")
		return CircleAlerts(response.json())






class CircleAdminModule(SyncBaseClass):

	def _build_mediamap(self, mediaMap: list[dict[str, IO | BufferedReader]],
			target: MediaTarget, content: str) -> tuple[dict, str]:
		result = {}
		for x in mediaMap:
			key, value = next(iter(x.items()))
			mediaId = random_ascii_string(10, True)
			result[mediaId] = {
				"src": self.upload_media(value, target).url,
				"isCover": False,
				"type": 0
			}
			content = content.replace(
				f"![{key}]", f"![{mediaId}](mediamap://{mediaId})"
			)
		return result, content

	@require_auth
	def get_circle_join_requests(self, circleId: str, size: str = 25, pageToken: str | None = None) -> JoinRequestList:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/admin/join-requests?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return JoinRequestList(response.json())
	

	@require_auth
	def resolve_circle_join_request(self, circleId: str, userId: str, isApproved: bool = True):
		self.req.make_request("POST", f"/{circleId}/s/circles/admin/join-requests/{userId}/resolve", {
			"isApproved": isApproved
		})
	
	@require_auth
	def hide_user(self, circleId: str, userId: str, note: str | None = None) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId}/s/users/{userId}/hide", {
			"note": note or ''
		})
		return UserProfile((response.json()).get("userProfile", {}))

	@require_auth
	def unhide_user(self, circleId: str, userId: str, note: str | None = None) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId}/s/users/{userId}/unhide", {
			"note": note or ''
		})
		return UserProfile((response.json()).get("userProfile", {}))

	@require_auth
	def strike_user(self, circleId: str, userId: str, message: str, muteTime: str = MuteDuration.ONE_HOUR):
		self.req.make_request("POST", f"/{circleId}/s/notices", {
			"uid": userId,
			"content": message,
			"time": muteTime
		})


	@require_auth
	def revoke_strike_user(self, circleId: str, userId: str, note: str | None = None) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId}/s/users/{userId}/revoke-strike", {
			"note": note or ''
		})
		return UserProfile((response.json()).get("userProfile", {}))

	@require_auth
	def warn_user(self, circleId: str, userId: str, message: str):
		self.req.make_request("POST", f"/{circleId}/s/notices", {
			"uid": userId,
			"content": message,
		})


	@require_auth
	def ban_user(self, circleId: str, userId: str, message: str | None = None) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId}/s/users/{userId}/ban", {
			"note": message or ''
		})
		return UserProfile((response.json()).get("userProfile", {}))


	@require_auth
	def unban_user(self, circleId: str, userId: str, message: str | None = None) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId}/s/users/{userId}/unban", {
			"note": message or ''
		})
		return UserProfile((response.json()).get("userProfile", {}))
	



	@require_auth
	def edit_user_titles(
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

		response = self.req.make_request(
			"POST",
			f"/{circleId}/s/users/{userId}/titles",
			{"titleList": title_list}
		)

		data = response.json()
		return UserProfile(data.get("userProfile", {}))



	@require_auth
	def delete_circle(self, circleId: str, password: str) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/delete", {
			"secret": password,
		})

		return Circle((response.json()).get("circle", {}))
	



	@require_auth
	def get_reports_count(self, circleId: str) -> int:
		response = self.req.make_request("GET", f"/{circleId}/s/reports/pending-count")

		return (response.json()).get("reportCount", 0)
	

	@require_auth
	def get_join_requests_count(self, circleId: str) -> int:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/admin/join-requests/count")
		return (response.json()).get("membersPendingCount", 0)

	@require_auth
	def get_posts_count(self, circleId: str) -> int:
		response = self.req.make_request("GET", f"/{circleId}/s/posts/count")
		return (response.json()).get("postCount", 0)


	@require_auth
	def check_alerts(self, circleId: str) -> UserAlerts:
		response = self.req.make_request("GET", f"/{circleId}/s/alerts/check")
		return UserAlerts(response.json())
	

	@require_auth
	def edit_circle_privacy(self, circleId: str, joinPermission: int = CirclePrivacy.Open) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"privacy": joinPermission
		})
		return Circle((response.json()).get("circle", {}))
	
	@require_auth
	def create_invite_link(self, circleId: str) -> CircleInviteLink:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/invites")
		return CircleInviteLink((response.json()).get("invite", {}))

	@require_auth
	def delete_invite_link(self, circleId: str):
		self.req.make_request("POST", f"/{circleId}/s/circles/invites/delete")
	

	@require_auth
	def edit_circle_vanity(self, circleId: str, vanity: str) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/vanity", {
			"vanity": vanity
		})
		return Circle((response.json()).get("circle", {}))
	
	@require_auth
	def check_circle_listing_tasks(self, circleId: str) -> CircleListingTasks:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/admin/listing/tasks")
		return CircleListingTasks(response.json())
	
	@require_auth
	def check_circle_stats(self, circleId: str) -> CircleAdminStats:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/admin/stats")
		return CircleAdminStats(response.json())
	
	@require_auth
	def get_circle_reports(self, circleId: str, size: str = 25, pageToken: str | None = None) -> CircleReportList:
		response = self.req.make_request("GET", f"/{circleId}/s/reports?type=pending&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return CircleReportList(response.json())
	
	@require_auth
	def get_circle_audit_logs(self, circleId: str, size: str = 25, pageToken: str | None = None):
		response = self.req.make_request("GET", f"/{circleId}/s/audit-logs?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return AuditLogList(response.json())
	
	@require_auth
	def get_search_chats(self, circleId: str, size: int = 25, pageToken: str | None = None, query: str | None = None) -> ChatsList:
		response = self.req.make_request("GET", f"/{circleId}/s/chats?type=search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return ChatsList(response.json())

	@require_auth
	def get_search_circle_posts(self, circleId: str, size: int = 25, pageToken: str | None = None, query: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=search&size={size}{f'&t={pageToken}' if pageToken else ''}{f'&q={query}' if query else ''}")
		return PostList(response.json())

	@require_auth
	def get_search_users(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId}/s/users?type=search&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())


	@require_auth
	def get_banned_users(self, circleId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId}/s/users?type=banned&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())

	@require_auth
	def get_staff_users(self, circleId: str, type: str = CircleUsersStaffType.Invited, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId}/s/users?type={type}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())

	@require_auth
	def edit_circle_chats_permission(self, circleId: str, chatRoomPermission: int = ChatRoomPermission.Anyone) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"chatRoomPermission": chatRoomPermission
		})
		return Circle((response.json()).get("circle", {}))

	@require_auth
	def edit_circle_article_permission(self, circleId: str, articlePermission: int = ArticlePermission.Anyone) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"articlePermission": articlePermission
		})
		return Circle((response.json()).get("circle", {}))

	@require_auth
	def edit_circle_threads_ermission(self, circleId: str, threadsPermission: int = ThreadsPermission.Anyone) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"threadsPermission": threadsPermission
		})
		return Circle((response.json()).get("circle", {}))

	@require_auth
	def edit_circle_wiki_permission(self, circleId: str, wikiPermission: int = WikiPermission.Anyone) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize", {
			"wikiPermission": wikiPermission
		})
		return Circle((response.json()).get("circle", {}))


	@require_auth
	def promote_to_circle_staff(self, circleId: str, userId: str, role: int = CircleRole.Moderator):
		self.req.make_request("POST", f"/{circleId}/s/users/{userId}/admin/promote", {
			"role": role
		})


	@require_auth
	def cancel_promote_to_circle_staff(self, circleId: str, userId: str):
		self.req.make_request("POST", f"/{circleId}/s/circles/admin/role-invites/{userId}/cancel")

	@require_auth
	def edit_circle(self, circleId: str, iconUrl: str, coverUrl: str, name: str, tagline: str, themeHexColor: str, isThemeDark: bool) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"iconUrl": iconUrl,
			"coverUrl": coverUrl,
			"name": name,
			"tagline": tagline,
			"themeColor": themeHexColor,
			"isThemeDark": isThemeDark
		})
		return Circle((response.json()).get("circle", {}))
	
	@require_auth
	def edit_circle_guideline(self, circleId: str, guidelines: str = "") -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"guidelines": guidelines
		})
		return Circle((response.json()).get("circle", {}))
	
	@require_auth
	def edit_circle_description(self, circleId: str, content: str = "", mediaMap: list[dict[str, IO | BufferedReader]] | None = None) -> Circle:
		payload = {
			"mediaMap": {}
		}

		if mediaMap:
			payload["mediaMap"], content = self._build_mediamap(
				mediaMap, MediaTarget.CircleIcon, content
			)
		payload["content"] = content

		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/edit", payload)
		return Circle((response.json()).get("circle", {}))

	@require_auth
	def get_circle_topics_list(self, circleId: str, size: int = 25, query: str | None = None) -> list[Topic]:
		response = self.req.make_request("GET", f"/{circleId}/s/circles/topics/?size={size}{f'&q={query}' if query else ''}")
		return [Topic(x) for x in (response.json()).get("topicList", [])]
	
	@require_auth
	def edit_circle_topics(self, circleId: str, topicIds: list[str]) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"topicIds": topicIds
		})
		return Circle((response.json()).get("circle", {}))

	@require_auth
	def edit_circle_sidebar_image(self, circleId: str, image: IO | BufferedReader) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/edit", {
			"sidebarCoverUrl": self.upload_media(image, MediaTarget.CircleSidebar).url
		})
		return Circle((response.json()).get("circle", {}))

	@require_auth
	def reorder_circle_pages(self, circleId: str, pageIds: list[str]) -> Circle:
		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize/home-layout/pages/reorder", {
			"pageIds": pageIds
		})
		return Circle((response.json()).get("circle", {}))


	@require_auth
	def delete_circle_page(self, circleId: str, pageId: str) -> Circle:
		response = self.req.make_request("DELETE", f"/{circleId}/s/circles/admin/customize/home-layout/pages/{pageId}")
		return Circle((response.json()).get("circle", {}))


	@require_auth
	def edit_circle_page(self, circleId: str, pageId: str, label: str, featuredLayout: int, content: str, pageType: str, isStartPage: bool = False) -> Circle:

		match pageType:
			case CirclePageType.WebPage:
				if not content:
					raise exceptions.ArgumentNeeded("For this page format, you must specify a link to the resource in the content argument")
			case CirclePageType.Post:
				if not content:
					raise exceptions.ArgumentNeeded("This page format requires you to specify a link to the post in the circle in the content argument")

		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize/home-layout/pages/{pageId}", {
			"id": pageId,
			"page": pageType,
			"label": label,
			"content": content,
			"featuredLayout": featuredLayout,
			"isStartPage": isStartPage
		})
		return Circle((response.json()).get("circle", {}))


	@require_auth
	def create_circle_page(self, circleId: str, label: str, featuredLayout: int = FeaturedLayoutTypes.Compact, content: str = "", pageType: str = CirclePageType.Guidlines, isStartPage: bool = False) -> Circle:

		match pageType:
			case CirclePageType.WebPage:
				if not content:
					raise exceptions.ArgumentNeeded("For this page format, you must specify a link to the resource in the content argument")
			case CirclePageType.Post:
				if not content:
					raise exceptions.ArgumentNeeded("This page format requires you to specify a link to the post in the circle in the content argument")


		response = self.req.make_request("POST", f"/{circleId}/s/circles/admin/customize/home-layout/pages", {
			"id": f"np-{strtime()}",
			"page": pageType,
			"label": label,
			"content": content,
			"featuredLayout": featuredLayout,
			"isStartPage": isStartPage
		})
		return Circle((response.json()).get("circle", {}))