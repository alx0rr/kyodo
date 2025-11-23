from . import BaseProfile



class CirclesList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.circles: list[Circle] = [Circle(circle) for circle in data.get("circles", [])]
		self.hasMore: bool = data.get("hasMore")

class CircleDiscoveryRequirements:
	def __init__(self, data: dict):
		self.data: dict = data
		self.isPublic: bool = data.get("isPublic")
		self.isBanned: bool = data.get("isBanned")
		self.passedAll: bool = data.get("passedAll")

		discovery: dict = data.get("discovery")
		members: dict = data.get("members")

		self.discoveryStatus: int = discovery.get("status")
		self.discoveryActive: bool = discovery.get("active")

		self.minMembersCount: int = members.get("min")
		self.currentMembersCount: int = members.get("current")
		self.passedMembers: bool = members.get("passed")

class Circle:
	def __init__(self, data: dict):
		self.data: dict = data
		self.id: str = data.get("id")
		self.vanity: str = data.get("id")
		self.icon: str = data.get("icon")
		self.banner: str = data.get("banner")
		self.name: str = data.get("name")
		self.language: str = data.get("language")
		self.primaryTopicId: str = data.get("primaryTopicId")
		self.memberCount: int = data.get("memberCount")
		self.theme: dict = data.get("theme")
		self.pageConfig: dict = data.get("pageConfig")
		self.moduleTypes: dict = data.get("moduleTypes")
		self.moduleConfig: dict = data.get("moduleConfig")
		self.isVerified: bool = data.get("isVerified")
		self.securityLevel: int = data.get("securityLevel")
		self.memberCount: int = data.get("memberCount")

		self.privacy: int = data.get("privacy")
		self.isNSFW: bool = data.get("isNSFW")
		self.status: int = data.get("status")
		self.dau: int = data.get("dau")
		self.createdTime: str = data.get("createdTime")

		self.discovery: dict = data.get("discovery")
		self.pinnedPost: dict = data.get("pinnedPost")
		self.geoBlocks: list = data.get("geoBlocks", [])

		self.owner: BaseProfile | None = BaseProfile(data.get("owner")) if data.get("owner") else None
		self.memberPreview: list[BaseProfile] | None = [BaseProfile(member) for member in data.get("memberPreview", [])] if data.get("memberPreview") else None
		self.staffPreview: list[BaseProfile] | None = [BaseProfile(staff) for staff in data.get("staffPreview", [])] if data.get("staffPreview") else None

		self.meInCircle: BaseProfile = BaseProfile(data.get("joinedUser", {}))


class CircleInfo:
	def __init__(self, data: dict):
		self.data: dict = data
		self.me: BaseProfile = BaseProfile(data.get("user"))
		self.circle: Circle = Circle(data.get("circle"))




class CircleStats:
	def __init__(self, data: dict):
		self.data: dict = data
		self.id: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")
		self.yesterdayMemberCount: int = data.get("yesterdayMemberCount")
		self.todayMemberCount: int = data.get("todayMemberCount")
		self.yesterdayDau: int = data.get("yesterdayDau")
		self.todayDau: int = data.get("todayDau")
		self.todayMau: int = data.get("todayMau")
		self.yesterdayMessageCount: int = data.get("yesterdayMessageCount")
		self.todayMessageCount: int = data.get("todayMessageCount")
		self.yesterdayPostCount: int = data.get("yesterdayPostCount")
		self.todayPostCount: int = data.get("todayPostCount")