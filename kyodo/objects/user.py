

class Title:
	def __init__(self, data: dict):
		self.data = data
		self.slug: str = self.data.get("slug")
		self.text: str = self.data.get("text")
		self.isGlobal: bool = self.data.get("global")
		self.bgColor: str = self.data.get("bgColor")
		self.fontColor: str = self.data.get("fontColor")



class BaseProfile:
	def __init__(self, data: dict):
		self.data = data
		self.userId: str = data.get("id")
		self.intId: int = data.get("intId")
		self.circleId: str = data.get("circleId")
		self.banner: str = data.get("banner") #idk
		self.avatar: str = data.get("avatar") #idk
		self.nickname: str = data.get("nickname")
		self.handle: str = data.get("handle")
		self.gRole: int = data.get("gRole")
		self.role: int = data.get("role")
		self.botType: int = data.get("botType")
		self.premiumType: int = data.get("premiumType")
		self.gStatus: int = data.get("gStatus")
		self.status: int = data.get("status")
		self.isVerified: bool = data.get("isVerified")
		self.joined: bool = data.get("joined")
		self.isOnline: bool = data.get("isOnline")
		self.lastOnline: str = data.get("lastOnline")
		self.followerCount: int = data.get("followerCount")
		self.followingCount: int = data.get("followingCount")
		self.commentCount: int = data.get("commentCount")
		self.createdTime: str = data.get("createdTime")
		self.titles = [Title(title) for title in (self.data.get("titles", []))]

		adminInfo: dict = data.get("adminInfo", {})
		bannerTheme: dict = data.get("bannerTheme", {})
		
		self.trustLevel: str = adminInfo.get("trustLevel")
		self.bannerDominant: str = bannerTheme.get("dominant")
		self.bannerFgColor: str = bannerTheme.get("fgColor")


class UsersList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.users: list[BaseProfile] = [BaseProfile(user) for user in data.get("users", [])]
		self.hasMore: bool = data.get("hasMore")


class UserActivity:
	def __init__(self, data: dict):
		self.data: dict = data
		self.userId: str = data.get("uid")
		self.today: int = data.get("today")
		self.week: int = data.get("week")
		self.weekAvg: int = data.get("weekAvg")


class HandleInfo:
	def __init__(self, data: dict):
		self.data: dict = data
		self.accountId: str = data.get("accountId")
		self.apiPath: str = data.get("apiPath")
		self.appPath: str = data.get("appPath")
		self.inUse: bool = data.get("inUse")


class AccountConfig:
	def __init__(self, data: dict):
		self.data: dict = data
		self.adsEnabled: bool = data.get("adsEnabled")
		self.storeEnabled: bool = data.get("storeEnabled")
		self.avatarFramesEnabled: bool = data.get("avatarFramesEnabled")
		self.hasBirthday: bool = data.get("hasBirthday")
		self.isLegalAge: bool = data.get("isLegalAge")
		self.versionOutdated: bool = data.get("versionOutdated")
		self.handleUpdateAvailable: bool = data.get("handleUpdateAvailable")
		self.handleUpdateAvailableTime: int | None = data.get("handleUpdateAvailableTime")


class UserPersona:
	def __init__(self, data: dict):
		self.data: dict = data
		self.avatar: str = data.get("avatar")
		self.userId: str = data.get("uid")
		self.status: int = data.get("status")
		self.personaId: str = data.get("id")
		self.nickname: str = data.get("nickname")
		self.content: str = data.get("content")
		self.updatedTime: str = data.get("updatedTime")
		self.createdTime: str = data.get("createdTime")
		self.circleId: str = data.get("circleId")
		self.theme: dict = data.get("theme", {})
		self.user: BaseProfile = BaseProfile(data.get("user", {}))

class UserPersonasList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.persona: list[UserPersona] = [UserPersona(persona) for persona in data.get("list" , [])]
		self.hasMore: bool = data.get("hasMore")