from kyodo.objects.args.object_types import KyodoObjectTypes


class AvatarFrame:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.id: str = data.get("id")
        self.icon: str = data.get("icon")
        self.resource: str = data.get("resource")
        self.name: str = data.get("name")
        self.status: int = data.get("status")
        self.version: int = data.get("version")
        self.restrictionType: int = data.get("restrictionType")
        self.ownershipStatus: int = data.get("ownershipStatus")


class AvatarFrameList:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.pagination: dict = data.get("pagination", {})
        self.avatarFrameList: list[AvatarFrame] = [AvatarFrame(x) for x in data.get("avatarFrameList", [])]





class ChatBubble:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: str = data.get("icon")
        self.cover: str = data.get("cover")
        self.resource: str = data.get("resource")
        self.status: int = data.get("status")
        self.userId: str = data.get("uid")
        self.version: int = data.get("version")
        self.isListed: bool = data.get("isListed`")
        self.listedTime: str = data.get("listedTime")
        self.restrictionType: int = data.get("restrictionType")
        self.createdTime: str = data.get("createdTime")
        self.modifiedTime: str = data.get("modifiedTime")

        self.config: dict = data.get("config")


class ChatBubbleList:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.pagination: dict = data.get("pagination", {})
        self.chatBubbleList: list[ChatBubble] = [ChatBubble(x) for x in data.get("chatBubbleList", [])]

class BannerInfo:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.mediaUrl: str = data.get("mediaUrl")



class StoreSection:
    def __init__(self, data: dict):
        data = data or {}
        self.data = data

        self.id: str = data.get("id")
        self.objectType: int = data.get("objectType")
        self.type: int = data.get("type")
        self.title: str = data.get("title")
        self.hasMore: bool = data.get("hasMore", False)

        self.items: AvatarFrame | ChatBubble | dict = []

        if self.objectType == KyodoObjectTypes.AvatarFrame:
            self.items = [AvatarFrame(x) for x in data.get("data", [])]

        elif self.objectType == KyodoObjectTypes.ChatBubble:
            self.items = [ChatBubble(x) for x in data.get("data", [])]

        else:
            self.items = data.get("data", [])  # fallback

class StoreItems:
    def __init__(self, data: dict):
        data = data or {}
        self.data = data

        self.code: int = data.get("code")
        self.apiCode: int = data.get("apiCode")
        self.message: str = data.get("message")

        self.banner: BannerInfo = BannerInfo(data.get("bannerInfo", {}))

        self.sections: list[StoreSection] = [
            StoreSection(x) for x in data.get("sectionList", [])
        ]