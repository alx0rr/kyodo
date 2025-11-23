


class ShareLink:
	def __init__(self, data: dict):
		self.data: dict = data
		share_link: dict = data.get("shareLink", {})
		if not share_link:
			share_link=data
		self.id: str = share_link.get("id")
		self.circleId: str = share_link.get("circleId")
		self.objectId: str = share_link.get("objectId")
		self.objectType: int = share_link.get("objectType")
		self.shareLink: str = share_link.get("shareLink")
		self.apiPath: str = share_link.get("apiPath")
		self.appPath: str = share_link.get("appPath")
		self.isVanity: bool = share_link.get("isVanity")
		self.createdTime: str = share_link.get("createdTime")
		self.updatedTime: str = share_link.get("updatedTime")
		self.isCircleJoined: bool = data.get("isCircleJoined")
		