from kyodo.objects.user import UserProfile

class CircleTheme:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.isDark: bool = self.data.get("isDark")
        self.fgColor: str = self.data.get("fgColor")
        self.dominant: str = self.data.get("dominant")


class ModuleBase:
    def __init__(self, data: dict):
        data = data or {}
        self.enabled = data.get("enabled", False)
        self.permission = data.get("permission")


class PostsModule:
    def __init__(self, data: dict):
        data = data or {}
        self.wikis = ModuleBase(data.get("wikis"))
        self.threads = ModuleBase(data.get("threads"))
        self.articles = ModuleBase(data.get("articles"))
        self.featured_layout = data.get("featuredLayout")


class CircleModules:
    def __init__(self, data: dict):
        data = data or {}

        self.posts = PostsModule(data.get("posts"))
        self.topics = ModuleBase(data.get("topics"))
        self.personas = ModuleBase(data.get("personas"))
        self.chat_rooms = ModuleBase(data.get("chatRooms"))

        leaderboard = data.get("leaderboard") or {}
        self.leaderboard_enabled = leaderboard.get("enabled", False)


class Circle:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.circleId: str = data.get("id")
        self.userId: str = data.get("userId")
        self.cover_url: str = data.get("cover")
        self.icon_url: str = data.get("icon")
        self.sidebarCover: str | None = data.get("sidebarCover")
        self.name: str = data.get("name")
        self.isVerified: bool = data.get("isVerified")
        self.privacy: int = data.get("privacy")
        self.vanity: str = data.get("vanity")
        self.status: int = data.get("status")
        self.theme: CircleTheme = CircleTheme(data.get("theme", {}))
        self.memberCount: int = data.get("memberCount")
        self.homeLayout: list[dict] = data.get("homeLayout")
        self.homeLayoutStartLabel: str = data.get("homeLayoutStartLabel")
        self.modules: CircleModules = CircleModules(data.get("modules", {}))
        self.tagline: str = data.get("tagline")
        self.language: str = data.get("language")
        self.isFeatured: bool = data.get("isFeatured")
        self.isListed: bool = data.get("isListed")
        self.listingStatus: int = data.get("listingStatus")
        self.createdTime: str = data.get("createdTime")
        self.modifiedTime: str = data.get("modifiedTime")
        self.topicIds: list[str] = data.get("topicIds")
        self.extensions: dict = data.get("extensions")
        self.userProfile: UserProfile = UserProfile(data.get("userProfile", {}))



class CircleList:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data
        self.circleList: list[Circle] = [Circle(x) for x in data.get("circleList", [])]
        self.pagination: dict = data.get("pagination")

class CircleInfo:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data
        
        self.userProfile: UserProfile = UserProfile(data.get("userProfile", {}))

        circle: dict = data.get("circle", {})
        circle.update({"userProfile": self.userProfile.data})
        self.circle = Circle(circle)
        self.composableFeatureList: list[str] = data.get("composableFeatureList")
        self.isMember: bool = data.get("isMember", False)



class ExploreModule:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data
        
        self.id: str = data.get("id")
        self.displayName: str = data.get("displayName")
        self.type: int = data.get("type")

        self.circleList: list[Circle] = [Circle(x) for x in data.get("circleList", [])]