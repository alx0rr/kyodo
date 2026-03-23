

class ChatMessageTypes:
    Text: int = 0
    Photo: int = 2
    Video: int = 3
    Sticker: int = 16


class ChatType:
    PRIVATE = 0
    GROUP = 1
    PUBLIC = 2




class ChatMemberTypes:
    All: str = "all"
    Host: str = "host"
    CoHosts: str = "co-hosts"
    ElegibleHosts: str = "elegible-hosts",
    ChatInviteEligible: str = "chat-invite-eligible"
    Kicked: str = "kicked"


    _all = [Host, CoHosts, All]
