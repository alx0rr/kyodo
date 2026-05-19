from kyodo.api.base import AsyncBaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.objects import Blog, PostList, PersonaList, Persona, MediaTarget, Poll, BlogTypes
from kyodo.utils.generators import random_ascii_string, strtime


from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader

class BlogModule(AsyncBaseClass):

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
	async def get_kyodo_team_posts(self, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/g/s/posts?type=team-kyodo&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())

	@require_auth
	async def get_recent_posts(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=latest&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())

	@require_auth
	async def get_pinned_posts(self, circleId: str, size: int = 100, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=pinned&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())

	@require_auth
	async def get_featured_posts(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=featured&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())


	@require_auth
	async def get_circle_wikis(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=wiki&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())



	@require_auth
	async def get_user_wikis(self, circleId: str, userId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=user-wikis&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())


	@require_auth
	async def get_user_posts(self, circleId: str, userId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=user-posts&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PostList(await response.json())

	@require_auth
	async def get_user_personas(self, circleId: str, userId: str, size: int = 25, pageToken: str | None = None) -> PersonaList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=user-personas&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return PersonaList(await response.json())


	@require_auth
	@require_uid
	async def get_my_personas(self, circleId: str, size: int = 25, pageToken: str | None = None) -> PersonaList:
		return await self.get_user_personas(circleId, self.userId, size, pageToken)


	@require_auth
	async def get_post_info(self, circleId: str, postId: str) -> Blog:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts/{postId}")
		return Blog((await response.json()).get("post", {}))
	
	@require_auth
	async def get_persona_info(self, circleId: str, personaId: str) -> Persona:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/personas/{personaId}")
		return Persona((await response.json()).get("persona", {}))


	@require_auth
	async def get_post_comments(self, circleId: str, postId: str, size: int = 25, pageToken: str | None = None) -> PostList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=thread&size={size}{f'&t={pageToken}' if pageToken else ''}&parentId={postId}")
		return PostList(await response.json())

	@require_auth
	async def toggle_post_like(self, circleId: str, postId: str) -> Blog:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/posts/{postId}/like")
		return Blog((await response.json()).get("post", {}))


	@require_auth
	async def delete_post(self, circleId: str, postId: str):
		await self.req.make_async_request("DELETE", f"/{circleId}/s/posts/{postId}")


	@require_auth
	async def delete_persona(self, circleId: str, personaId: str) -> Persona:
		response = await self.req.make_async_request("DELETE", f"/{circleId}/s/personas/{personaId}")
		return Persona((await response.json()).get("persona", {}))


	async def vote_post_poll(self, poolId: str, optionId: str) -> Poll:
		response = await self.req.make_async_request("POST", f"/s/polls/{poolId}/options/{optionId}/vote")
		return Poll((await response.json()).get("poll", {}))



	def _build_attributes(self, attributes: list[dict[str, str]]) -> list[dict]:
		result = []
		base_time = int(strtime())
		for i, attr in enumerate(reversed(attributes)):
			result.append({
				"id": f"idx_{base_time - (i + 1)}",
				"title": attr["title"],
				"text": attr["text"]
			})
		result.reverse()
		return result

	async def _apply_background(self, payload: dict, backgroundImage, target: MediaTarget,
			background_color: str | None, text_color: str | None):
		if backgroundImage:
			payload["background"] = {
				"src": (await self.upload_media(backgroundImage, target)).url
			}
		elif background_color and text_color:
			payload["background"] = {
				"background": background_color,
				"text": text_color
			}



	async def create_post_thread(self, circleId: str, content: str, poll: list[str], mediaList: list[IO | BufferedReader] | None = None) -> Blog:
		
		payload = {
			"content": content,
			"type": BlogTypes.thread,
			"mediaList": [],
		}

		if mediaList:
			for x in mediaList:
				payload["mediaList"].append(
					(await self.upload_media(x, MediaTarget.PostGallery)).url
				)
		
		if poll:
			payload["poll"] = []
			for x in poll:
				payload["poll"].append({"text": x})


		response = await self.req.make_async_request("POST", f"/{circleId}/s/posts", payload)
		return Blog((await response.json()).get("post", {}))



	async def create_post_article(self, circleId: str, title: str, content: str,
			poll: list[str],
			background_color: str | None = None, text_color: str | None = None,
			mediaMap: list[dict[str, IO | BufferedReader]] | None = None,
			coverImage: IO | BufferedReader | None = None,
			backgroundImage: IO | BufferedReader | None = None) -> Blog:

		payload = {
			"title": title,
			"type": BlogTypes.article,
			"mediaMap": {},
		}

		await self._apply_background(payload, backgroundImage, MediaTarget.PostGallery,
							background_color, text_color)

		if poll:
			payload["poll"] = [{"text": x} for x in poll]

		if coverImage:
			payload["mediaMap"]["cover"] = {
				"src": (await self.upload_media(coverImage, MediaTarget.PostGallery)).url,
				"isCover": True,
				"type": 0
			}

		if mediaMap:
			media, content = await self._build_mediamap(mediaMap, MediaTarget.PostGallery, content)
			payload["mediaMap"].update(media)

		payload["content"] = content
		response = await self.req.make_async_request("POST", f"/{circleId}/s/posts", payload)
		return Blog((await response.json()).get("post", {}))


	async def create_post_wiki(self, circleId: str, title: str, content: str,
			attributes: list[dict[str, str]],
			coverImage: IO | BufferedReader,
			background_color: str | None = None, text_color: str | None = None,
			mediaMap: list[dict[str, IO | BufferedReader]] | None = None,
			backgroundImage: IO | BufferedReader | None = None) -> Blog:

		payload = {
			"title": title,
			"type": BlogTypes.wiki,
			"attributes": self._build_attributes(attributes),
			"mediaMap": {
				"cover": {
					"src": (await self.upload_media(coverImage, MediaTarget.PostGallery)).url,
					"isCover": True,
					"type": 0
				}
			},
		}

		await self._apply_background(payload, backgroundImage, MediaTarget.PostGallery,
							background_color, text_color)

		if mediaMap:
			media, content = await self._build_mediamap(mediaMap, MediaTarget.PostGallery, content)
			payload["mediaMap"].update(media)

		payload["content"] = content
		response = await self.req.make_async_request("POST", f"/{circleId}/s/posts", payload)
		return Blog((await response.json()).get("post", {}))


	async def create_persona(self, circleId: str, nickname: str, content: str,
			avatarImage: IO | BufferedReader,
			attributes: list[dict[str, str]] | None = None,
			background_color: str | None = None, text_color: str | None = None,
			mediaMap: list[dict[str, IO | BufferedReader]] | None = None,
			backgroundImage: IO | BufferedReader | None = None) -> Persona:

		payload = {
			"nickname": nickname,
			"avatar": (await self.upload_media(avatarImage, MediaTarget.PersonaAvatar)).url,
			"attributes": self._build_attributes(attributes) if attributes else [],
			"mediaMap": {},
		}

		await self._apply_background(payload, backgroundImage, MediaTarget.PersonaGallery,
							background_color, text_color)

		if mediaMap:
			media, content = await self._build_mediamap(mediaMap, MediaTarget.PersonaGallery, content)
			payload["mediaMap"].update(media)

		payload["content"] = content
		response = await self.req.make_async_request("POST", f"/{circleId}/s/personas", payload)
		return Persona((await response.json()).get("persona", {}))