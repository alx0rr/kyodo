from kyodo.api.base import SyncBaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.objects import Blog, PostList, PersonaList, Persona

class BlogModule(SyncBaseClass):



	@require_auth
	def get_kyodo_team_posts(self, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/g/s/posts?type=team-kyodo&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())

	@require_auth
	def get_recent_posts(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=latest&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())

	@require_auth
	def get_pinned_posts(self, circleId: str, size: int = 100, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=pinned&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())

	@require_auth
	def get_featured_posts(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=featured&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())


	@require_auth
	def get_circle_wikis(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=wiki&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())



	@require_auth
	def get_user_wikis(self, circleId: str, userId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=user-wikis&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())


	@require_auth
	def get_user_posts(self, circleId: str, userId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=user-posts&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(response.json())

	@require_auth
	def get_user_personas(self, circleId: str, userId: str, size: int = 25, pageToken: str | None = None) -> PersonaList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=user-personas&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PersonaList(response.json())


	@require_auth
	@require_uid
	def get_my_personas(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PersonaList:
		return self.get_user_personas(circleId, self.userId, size, pageToken)


	@require_auth
	def get_post_info(self, circleId: str, postId: str) -> Blog:
		response = self.req.make_request("GET", f"/{circleId}/s/posts/{postId}")
		return Blog((response.json()).get("post", {}))
	
	@require_auth
	def get_persona_info(self, circleId: str, personaId: str) -> Persona:
		response = self.req.make_request("GET", f"/{circleId}/s/personas/{personaId}")
		return Persona((response.json()).get("persona", {}))


	@require_auth
	def get_post_comments(self, circleId: str, postId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = self.req.make_request("GET", f"/{circleId}/s/posts?type=thread&size={size}{f'&t={pageToken}' if pageToken else ''}&parentId={postId}")
		return PostList(response.json())

	@require_auth
	def toggle_post_like(self, circleId: str, postId: str) -> Blog:
		response = self.req.make_request("POST", f"/{circleId}/s/posts/{postId}/like")
		return Blog((response.json()).get("post", {}))


	@require_auth
	def delete_post(self, circleId: str, postId: str):
		self.req.make_request("DELETE", f"/{circleId}/s/posts/{postId}")


	@require_auth
	def delete_persona(self, circleId: str, personaId: str) -> Persona:
		response = self.req.make_request("DELETE", f"/{circleId}/s/personas/{personaId}")
		return Persona((response.json()).get("persona", {}))