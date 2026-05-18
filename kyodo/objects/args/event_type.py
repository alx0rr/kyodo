


class EventType:

    ANY: str = "ANY_EVENT"

    ChatMessage: int = 1
    DeleteMessage: int = 2

    ChatTextMessage: str = "1:0"
    ChatImageMessage: str = "1:2"
    ChatMemberJoin: str = "1:5"
    ChatMemberLeave: str = "1:6"
    VoiceChatStarted: str = "1:14"
    VoiceChatEnded: str = "1:15"
    ChatStickerMessage: str = "1:16"

    OpenChatScreen: int = 6
    Ping: int = 7
    Typing: int = 16
    TypingEnd: int = 17
    #Notification: int = 18
    CircleProfileInfo: int = 24

    GeneralNotice: int = 25
    Notification: int = "25:notification"
    Notice: str = "25:notice"

    OpenCircleScreen: int = 26
    CloseCircleScreen: int = 27
    ChatInvite: int = 29