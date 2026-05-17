
from kyodo.utils import log
from kyodo.objects import EventType
from kyodo.objects.ws_events import (
    BaseEvent, WSDeletedMessage, WSChatMessage,
    WSChatInvite, WSChatTyping, WSChatTypingEnd

)
from kyodo.ws import MiddlewareStopException
from kyodo.ws._async.router import AsyncRouter
import asyncio
from typing import Callable


class Handler(AsyncRouter):
    def __init__(self):
        super().__init__()

    async def handle_data(self, _data: dict):
        data: dict = _data.get("d", {})
        _o = _data.get("o")
        await self.call(data, _o)

    async def call(self, data: dict, type: str):
        match type:
            case EventType.ChatMessage:
                sub_type = data.get("chatMessage", {}).get("type")
                data = WSChatMessage(self, type, data, sub_type)
            case EventType.DeleteMessage:
                sub_type = None
                data = WSDeletedMessage(self, type, data, sub_type)
            case EventType.Typing:
                sub_type = None
                data = WSChatTyping(self, type, data, sub_type)
            case EventType.TypingEnd:
                sub_type = None
                data = WSChatTypingEnd(self, type, data, sub_type)
            case EventType.ChatInvite:
                sub_type = None
                data = WSChatInvite(self, type, data, sub_type)
            case _:
                sub_type = None
                data = BaseEvent(self, type, data, sub_type)






        try:
            await self._run_middlewares(data, type, sub_type)
        except MiddlewareStopException:
            log.debug(f"[ws][middleware] Event {type} stopped by middleware")
            return

        keys = (EventType.ANY, type, f"{type}:{sub_type}")

        tasks = []
        for key in keys:
            if key not in self.handlers:
                continue
            for func in self.handlers[key]:
                tasks.append(self._invoke_handler(func, data))

        if tasks:
            await asyncio.gather(*tasks)

    async def _invoke_handler(self, func: Callable, data):
        try:
            if asyncio.iscoroutinefunction(func):
                await func(data)
            else:
                await asyncio.get_event_loop().run_in_executor(None, func, data)
        except Exception as e:
            log.error(f"[ws][event][{func}] Error: {e}")

    async def _run_middlewares(self, data, type: str, sub_type=None):
        middlewares_to_run = []

        for key in (EventType.ANY, type, f"{type}:{sub_type}" if sub_type else None):
            if key and key in self.middlewares:
                middlewares_to_run.extend(self.middlewares[key])

        for middleware in middlewares_to_run:
            try:
                if asyncio.iscoroutinefunction(middleware):
                    result = await middleware(data)
                else:
                    result = await asyncio.get_event_loop().run_in_executor(None, middleware, data)

                if result is False:
                    raise MiddlewareStopException()
            except MiddlewareStopException:
                raise
            except Exception as e:
                log.error(f"[ws][middleware][{middleware}] Error: {e}")