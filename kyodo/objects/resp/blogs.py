from kyodo.objects.resp.user import UserProfile


class Blog:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.postId: str = data.get("id")
        self.circleId: str = data.get("circleId")
        self.type: int = data.get("type")
        self.userId: str = data.get("uid")
        self.title: str = data.get("title")
        self.content: str = data.get("content")
        self.likeCount: int = data.get("likeCount")
        self.replyCount: int = data.get("replyCount")
        self.status: int = data.get("status")
        self.isPinned: bool = data.get("isPinned")
        self.isLiked: bool = data.get("isLiked")
        self.isFeatured: bool = data.get("isFeatured")
        self.createdTime: str = data.get("createdTime")
        self.modifiedTime: str = data.get("modifiedTime")
        self.user: UserProfile = UserProfile(data.get("user", {}))
        self.extensions: dict = data.get("extensions", {})
        self.mediaMap: dict = data.get("mediaMap", {})


class PostList:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.pagination: dict = data.get("pagination", {})
        self.postList: list[Blog] = [Blog(x) for x in data.get("postList", [])]



class Persona:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.postId: str = data.get("id")
        self.circleId: str = data.get("circleId")
        self.type: int = data.get("type")
        self.userId: str = data.get("uid")
        self.avatar: str = data.get("avatar")
        self.nickname: str = data.get("nickname")
        self.status: int = data.get("status")
        self.createdTime: str = data.get("createdTime")
        self.modifiedTime: str = data.get("modifiedTime")
        self.user: UserProfile = UserProfile(data.get("user", {}))
        self.extensions: dict = data.get("extensions", {})
        self.mediaMap: dict = data.get("mediaMap", {})


class PersonaList:
    def __init__(self, data: dict):
        data = data or {}
        self.data=data

        self.pagination: dict = data.get("pagination", {})
        self.personaList: list[Persona] = [Persona(x) for x in data.get("postList", [])]



class PollOption:
    def __init__(self, data: dict):
        data = data or {}
        self.data = data

        self.id: str = data.get("id")
        self.text: str = data.get("text")
        self.vote_count: int = data.get("voteCount", 0)
        self.is_voted: bool = data.get("isVoted", False)


class Poll:
    def __init__(self, data: dict):
        data = data or {}

        self.data = data

        self.id: str = data.get("id")
        self.circle_id: str = data.get("circleId")
        self.vote_count: int = data.get("voteCount", 0)
        self.is_voted: bool = data.get("isVoted", False)
        self.is_closed: bool = data.get("isClosed", False)
        self.created_time: str = data.get("createdTime")

        self.option_list: list[PollOption] = [
            PollOption(option)
            for option in data.get("optionList", [])
        ]