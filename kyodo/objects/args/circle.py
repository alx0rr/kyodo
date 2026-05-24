from enum import Enum

class CircleRole:
    Owner: int = 3
    Admin: int = 2
    Moderator: int = 1
    Member: int = 0


class MuteDuration:
    ONE_HOUR = '1h'
    SIX_HOURS = '6h'
    ONE_DAY = '1d'
    THREE_DAYS = '3d'
    SEVEN_DAYS = '7d'


class CircleUsersType:
    Mods: str = "mods"
    Admins: str = "admins"
    Online: str = "online"
    Members: str = "members"
    Owner: str = "owner"
    OnlineFollowing: str = "online-following"
    ChatInviteEligible: str = "chat-invite-eligible"


    _all = [Mods, Online, Admins, Owner, Members, OnlineFollowing]

class CircleUsersStaffType:
    Mods: str = "eligible-mods"
    Admins: str = "eligible-admins"
    Invited: str = "invited-staff"
    Owners: str = "eligible-owners"

class CirclePrivacy:
    Open: int = 1
    JoinRequestsOnly: int  = 2
    InviteOnly: int = 0


class CircleTemplate:
    FromScratch: int = 1


class CirclePageType:
    Chats: str = "chat-rooms"
    Featured: str = "featured"
    Leaderboard: str = "leaderboard"
    Guidlines: str = "guidelines"
    RecentPosts: str = "recent-posts"
    Wikis: str = "wikis"
    WebPage: str = "webview"
    Post: str = "post"


class FeaturedLayoutTypes:
    Relaxed: int = 1
    Stacked: int = 2
    Compact: int = 3