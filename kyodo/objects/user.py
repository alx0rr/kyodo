from kyodo.objects.store import AvatarFrame


class AccountInfo:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.userId: str = data.get("uid")
		self.username: str = data.get("username")
		self.isEmailVerified: bool = data.get("isEmailVerified")
		self.premiumType: int = data.get("premiumType")
		self.premiumAcquireType: str = data.get("premiumAcquireType")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")
		self.email: str = data.get("email")

		self.extensions: dict = data.get("extensions", {})



class UserTitle:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data
		self.bg: str = data.get("bg")
		self.fg: str = data.get("fg")
		self.id: str = data.get("id")
		self.text: str = data.get("text")
		self.isOfficial: bool = data.get("isOfficial")


class UserProfile:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data


		self.userId: str = data.get("uid")
		self.circleId: str = data.get("circleId")
		self.avatar_url: str = data.get("avatar")
		self.avatarFrameId: str = data.get("avatarFrameId")
		self.cover_url: str = data.get("cover")
		self.nickname: str = data.get("nickname")
		self.username: str = data.get("username")
		self.status: int = data.get("status")
		self.isHidden: bool = data.get("isHidden")
		self.isJoined: bool = data.get("isJoined")
		self.role: int = data.get("role")
		self.followerCount: int = data.get("followerCount")
		self.followingCount: int = data.get("followingCount")
		self.chatPrivacy: int = data.get("chatPrivacy")
		self.isNicknameVerified: bool = data.get("isNicknameVerified")
		self.isOnline: bool = data.get("isOnline")
		self.premiumType: int = data.get("premiumType")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")
		self.bio: str = data.get("bio")

		self.activity: dict = data.get("activity", {})
		self.extensions: dict = data.get("extensions", {})
		self.titleList: list = data.get("titleList", [])
		self.avatarFrame: AvatarFrame = AvatarFrame(data.get("avatarFrame", {}))

		self.titleList: list[UserTitle] = [UserTitle(x) for x in data.get("titleList", [])]



class OnlinePreview:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.userId: str = data.get("uid")
		self.avatar: str = data.get("avatar")
		self.status: int = data.get("status")


class OnlineUsers:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data
		self.onlineUserCount: int = data.get("onlineUserCount")
		
		self.owners: list[UserProfile] = [UserProfile(x) for x in data.get("ownerList", {})]
		self.admins: list[UserProfile] = [UserProfile(x) for x in data.get("adminList", {})]
		self.mods: list[UserProfile] = [UserProfile(x) for x in data.get("modList", {})]
		self.users: list[UserProfile] = [UserProfile(x) for x in data.get("onlineUserList", {})]


class UserProfileList:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.pagination: dict = data.get("pagination", {})

		userProfileList = []
		if data.get("userProfileList"):
			userProfileList = data.get("userProfileList")
		if data.get("chatMemberList"):
			userProfileList = data.get("chatMemberList")

		self.userProfileList: list[UserProfile] = [UserProfile(x) for x in userProfileList]


class BlockingUsers:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.blockingList: list[str] = data.get("blockingList", [])
		self.blockList: list[str] = data.get("blockList", [])


class BlockingResult:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data
		
		self.isBlocked: bool = data.get("isBlocked")
		self.userProfile: UserProfile = UserProfile(data.get("userProfile", {}))


class BirthdayInfo:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.birthday: str = data.get("birthday")
		self.age: int = data.get("age")


class UserBadge:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.id: str = data.get("id")
		self.name: str = data.get("name")
		self.mediaUrl: str = data.get("mediaUrl")
		self.url: str = data.get("url")
		self.grantedTime: str = data.get("grantedTime")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")