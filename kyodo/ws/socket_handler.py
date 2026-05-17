from kyodo.utils import log
from kyodo.objects import EventType
from kyodo.objects.ws_events import (
    BaseEvent, WSDeletedMessage, WSChatMessage,
    WSChatInvite, WSChatTyping, WSChatTypingEnd

)
from kyodo.ws import MiddlewareStopException
from kyodo.ws.router import Router


class Handler(Router):
    """Dispatches incoming socket events to registered handlers"""

    def __init__(self):
        super().__init__()

    def handle_data(self, _data: dict):
        data: dict = _data.get("d", {})
        _o = _data.get("o")
        self.call(data, _o)

    def call(self, data: dict, type: str):
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
            self._run_middlewares(data, type, sub_type)
        except MiddlewareStopException:
            log.debug(f"[ws][middleware] Event {type} stopped by middleware")
            return

        for key in (EventType.ANY, type, f"{type}:{sub_type}"):
            if key not in self.handlers:
                continue
            for func in self.handlers[key]:
                try:
                    func(data)
                except Exception as e:
                    log.error(f"[ws][event][{func}] Error: {e}")

    def _run_middlewares(self, data, type: str, sub_type=None):
        middlewares_to_run = []

        for key in (EventType.ANY, type, f"{type}:{sub_type}" if sub_type else None):
            if key and key in self.middlewares:
                middlewares_to_run.extend(self.middlewares[key])

        for middleware in middlewares_to_run:
            try:
                result = middleware(data)
                if result is False:
                    raise MiddlewareStopException()
            except MiddlewareStopException:
                raise
            except Exception as e:
                log.error(f"[ws][middleware][{middleware}] Error: {e}")