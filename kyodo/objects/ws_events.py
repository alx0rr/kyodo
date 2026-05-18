from __future__ import annotations

from .user import UserTyping, UserProfilePreview
from .chats import DeleteChatMessage, ChatMessage, Chat
from .common import Notice, Notification
from kyodo.utils.state import AsyncSafeState, ThreadSafeState


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kyodo.client import Client
    from kyodo.async_client import Client as AsyncClient


def createState(client: AsyncClient | Client, initial_dict: dict | None = None) -> ThreadSafeState | AsyncSafeState:
        
        from kyodo.client import Client
        from kyodo.async_client import Client as AsyncClient

        if isinstance(client, AsyncClient):
            return AsyncSafeState(initial_dict)

        if isinstance(client, Client):
            return ThreadSafeState(initial_dict)



class WSEventInfo:
    def __init__(self, type: int, sub_type: int | str | None = None):
        self.event_type = type
        self.sub_type = sub_type


class BaseEvent:
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        self.info = WSEventInfo(type, sub_type)
        self.client = client
        self.data = data
        self.state: AsyncSafeState | ThreadSafeState = createState(client)

class WSDeletedMessage(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.deletedMessage = DeleteChatMessage(self.data)


class WSChatMessage(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.message = ChatMessage(self.data.get("chatMessage"))
        self.chatId: str = self.data.get("chatId")
        self.circleId: str = self.data.get("circleId")
        self.chat = Chat(self.data.get("chat"))


class WSChatTyping(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.chatId: str = self.data.get("chatId")
        self.user = UserTyping(self.data.get("userProfile", {}))

class WSChatTypingEnd(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.chatId: str = self.data.get("chatId")
        self.userId: str = self.data.get("uid")


class WSChatInvite(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.chatId: str = self.data.get("chatId")
        self.circleId: str = self.data.get("circleId")
        self.chat = Chat(self.data.get("chat"))


class WSCircleProfileInfo(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.circleId: str = self.data.get("circleId")
        self.userCount: int = self.data.get("userCount")
        self.userProfilePreview = UserProfilePreview(self.data.get("userProfilePreview"))



class WSNotification(BaseEvent):
    def __init__(
        self,
        client: Client | AsyncClient,
        type: int,
        data: dict,
        sub_type: int | str | None = None
    ):
        super().__init__(client, type, data, sub_type)

        self.circleId: str = self.data.get("circleId")
        self.notice = Notice(self.data.get("notice")) if sub_type == "notice" else None
        self.notification = Notification(self.data.get("notification")) if sub_type == "notification" else None