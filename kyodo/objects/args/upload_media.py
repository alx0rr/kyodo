

SUPPORTED_MEDIA_FILES: tuple = ("video/mp4", "image/jpg", "image/png", "image/gif", "image/jpeg")


class MediaTarget:

	ChatVideoMessage: str = "chat-video"
	ChatImageMessage: str = "chat-message"
	CircleIcon: str = "circle-icon"
	ChatIcon: str = "chat-icon"
	ChatBackground: str = "chat-background"
	PostMedia: str = "post-media"
	UserBanner: str = "user-banner"
	UserAvatar: str = "user-avatar"
	StickerImage: str = "sticker"
	PersonaAvatar: str = "persona-avatar"



class MediaValue:
	def __init__(self, data: dict = {}):
		self.data = data

		self.url: str = self.data.get("mediaValue")
		self.pallet: dict = self.data.get("pallet", {}) #idk

	def __str__(self):
		return f"kyodo.MediaValue <url={self.url}>"