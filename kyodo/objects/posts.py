from . import BaseProfile


class PostInfo:
	def __init__(self, data: dict):
		self.data: dict = data
		self.postId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.title: str = data.get("title")
		self.content: str = data.get("content")
		self.type: int = data.get("type")
		self.isPinned: bool = data.get("isPinned")
		self.isHighlighted: bool = data.get("isHighlighted")
		self.likeCount: int = data.get("likeCount")
		self.replyCount: int = data.get("replyCount")
		self.status: int = data.get("status")
		self.stickerId: str | None = data.get("stickerId")
		self.liked: bool = data.get("liked")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")
		self.folderIds: list[str] = data.get("folderIds")
		self.mediaMap: dict = data.get("mediaMap", {})
		self.author: BaseProfile = BaseProfile(data.get("user"))


class PostsList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.chats: list[PostInfo] = [PostInfo(post) for post in data.get("posts", [])]
		self.hasMore: bool = data.get("hasMore")