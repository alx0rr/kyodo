from .base import BaseClass
from ..objects import (
	MediaTarget, UsersList, Folder,
	PostsList, PostInfo, FoldersList
)
from ..utils import require_auth, exceptions
from ..utils.generators import random_ascii_string, get_target_date

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader




class PostsModule(BaseClass):

	#post-folders-------------

	@require_auth
	async def delete_folder(self, circleId: str, folderId: str) -> bool:
		await self.req.make_async_request("DELETE", f"/{circleId}/s/posts/user/folders/{folderId}")
		return True

	@require_auth
	async def edit_folder_name(self, circleId: str, folderId: str, name: str) -> Folder:
		result = await self.req.make_async_request("PUT", f"/{circleId}/s/posts/user/folders/{folderId}/details", {"name": name})
		data = await result.json()
		return Folder(data["folder"])
		
	@require_auth
	async def get_folder_info(self, circleId: str, folderId: str) -> Folder:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts/user/folders/{folderId}/details")
		data: dict = await result.json()
		return Folder(data["folder"])

	@require_auth
	async def create_folder(self, circleId: str, name: str) -> Folder:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/posts/user/folders", {"name": name})
		data: dict = await result.json()
		return Folder(data["folder"])
	
	@require_auth
	async def edit_post_folders(self, circleId: str, postId: str, folderIds: list[str] | str) -> bool:
		if isinstance(folderIds, str): folderIds = [folderIds]
		await self.req.make_async_request("POST", f"/{circleId}/s/posts/user/folders/-/{postId}/edit", {"folderIds":folderIds})
		return True

	@require_auth
	async def get_folder_posts(self, circleId: str, folderId: int, limit: int = 15, start: int = 0) -> PostsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=6&limit={limit}&start={start}&parentId={folderId}")
		return PostsList(await result.json())
	
	@require_auth
	async def get_user_folders(self, circleId: str, userId: str, start: int = 0, limit: int = 100) -> FoldersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts/user/folders/{userId}?start={start}&limit={limit}")
		return FoldersList(await result.json())

	#posts--------------------------

	@require_auth
	async def highlight_post(self, circleId: str, postId: str, days: int = 1) -> dict:
		#doesn't work even in the app
		req = await self.req.make_async_request("POST", f"/{circleId}/s/posts/{postId}/highlight ", {
			"targetDate": get_target_date(days)
		})
		return await req.json()

	@require_auth
	async def disable_enable_post(self, circleId: str, postId: str, reason: str) -> bool:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/posts/{postId}/status",{
			"note": reason
		})
		data: dict = await result.json()
		return bool(data["objectStatus"])

	@require_auth
	async def pin_unpin_post(self, circleId: str, postId: str) -> bool:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/posts/{postId}/pin")
		data: dict = await result.json()
		return data.get("isPinned", False)

	@require_auth
	async def get_post_likes(self, circleId: str, postId: str, start: int = 0, limit: int = 15) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts/{postId}/likes?start={start}&limit={limit}")
		UsersList(await result.json())

	@require_auth
	async def delete_post(self, circleId: str, postId: str) -> bool:
		await self.req.make_async_request("DELETE", f"/{circleId}/s/posts/{postId}")
		return True

	@require_auth
	async def get_post_info(self, circleId: str, postId: str) -> PostInfo:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts/{postId}")
		data: dict = await result.json()
		return PostInfo(data["post"])
	
	@require_auth
	async def like_unlike_post(self, circleId: str, postId: str) -> bool:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts/{postId}/like")
		data: dict = await result.json()
		return data["isLiked"]

	@require_auth
	async def get_user_posts(self, circleId: str, userId: str, start: int = 0, limit: int = 15) -> PostsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=3&limit={limit}&start={start}&uid={userId}")
		return PostsList(await result.json())


	@require_auth
	async def get_circle_disabled_posts(self, circleId: str, start: int = 0, limit: int = 15) -> PostsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=5&limit={limit}&start={start}")
		return PostsList(await result.json())

	@require_auth
	async def get_circle_posts(self, circleId: str, start: int = 0, limit: int = 15) -> PostsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=0&limit={limit}&start={start}")
		return PostsList(await result.json())

	@require_auth
	async def comment_post(self, circleId: str, postId: str, content: str | None = None, stickerId: str | None = None) -> PostInfo:
		if not content and not stickerId:
			raise exceptions.NoDataError
		data = {
			"title": '-',
			"content": content or '-',
			"config":{
				"parentPostId": postId
				}
		}
		if stickerId:data["config"]["stickerId"] = stickerId

		result = await self.req.make_async_request("POST", f"/{circleId}/s/posts", data)
		data: dict = await result.json()
		return PostInfo(data["post"])



	@require_auth
	async def get_post_comments(self, circleId: str, postId: str, start: int = 0, limit: int = 15) -> PostsList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/posts?type=4&limit={limit}&start={start}&parentId={postId}")
		return PostsList(await result.json())

	@require_auth
	async def create_post(self, circleId: str, title: str, content: str, media_files: list[IO | BufferedReader | AsyncBufferedReader] | None = None, cover_image: IO | BufferedReader | AsyncBufferedReader | None = None) -> PostInfo:
		media_list = list()
		data = {
			"title": title,
			"content": content,
			"config":{
				"mediaMap":{}
				}
			}
	
		if media_files:
			for file in media_files:
				result = await self.upload_media(file, MediaTarget.PostMedia)
				media_list.append((result.url, 0, False))
		if cover_image:
			result = await self.upload_media(cover_image, MediaTarget.PostMedia)
			media_list.append((result.url, 0, True))
		
		for media in media_list:
				data["config"]["mediaMap"][random_ascii_string(7)]={
					"type": media[1],
					"src": media[0],
					"isCover": media[2]
				}

		result = await self.req.make_async_request("POST", f"/{circleId}/s/posts", data)
		data: dict = await result.json()
		return PostInfo(data["post"])
