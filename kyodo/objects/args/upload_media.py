

SUPPORTED_MEDIA_FILES: tuple = ("video/mp4", "image/jpg", "image/png", "image/gif", "image/jpeg")


class MediaTarget:

	ChatVideoMessage: str = "chat/video"

	CircleIcon: str = "circle/icon"
	ChatBackground: str = "chat/background"
	PostMedia: str = "post/media"

	ChatImageMessage: str = "chat/message"
	ChatIcon: str = "chat/icon"
	PostGallery: str = "post/gallery"
	UserBanner: str = "user/banner"
	UserAvatar: str = "user/avatar"
	StickerImage: str = "sticker"
	PersonaAvatar: str = "persona/icon"
	PersonaGallery: str = "persona/gallery"



class MediaValue:
	def __init__(self, data: dict = {}):
		if not data:data={}
		self.data=data

		media: dict = self.data.get("media", {})

		self.id: str = media.get("id", {})
		self.url: str = media.get("url")
		self.variants: dict = media.get("variants", {})

	def __str__(self):
		return f"kyodo.MediaValue <url={self.url}>"