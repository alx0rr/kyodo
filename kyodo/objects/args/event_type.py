


class EventType:

    ANY: str = "ANY_EVENT"

    ChatMessage: int = 1

    ChatTextMessage: str = "1:0"
    ChatImageMessage: str = "1:2"
    ChatMemberJoin: str = "1:5"
    ChatMemberLeave: str = "1:6"
    VoiceChatStarted: str = "1:14"
    VoiceChatEnded: str = "1:15"
    ChatStickerMessage: str = "1:16"

    OpenChatScreen: int = 6
    Ping: int = 7
    Notification: int = 18