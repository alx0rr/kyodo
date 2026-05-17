from __future__ import annotations

from .user import UserTyping
from .chats import DeleteChatMessage, ChatMessage, Chat


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kyodo.client import Client
    from kyodo.async_client import Client as AsyncClient


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