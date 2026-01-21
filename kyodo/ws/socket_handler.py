from ..utils import log
from traceback import format_exc
from ..objects import EventType, ChatMessage, BaseEvent, DeleteChatMessage

class MiddlewareStopException(Exception):
    """Exception to stop the handler chain"""
    pass

class Handler:
    """Module to create event handlers for sockets"""
    handlers: dict = {}
    middlewares: dict = {}

    async def handle_data(self, _data: dict):
        data: dict = _data.get("d", {})
        _o = _data.get("o")
        await self.call(data, _o)

    async def call(self, data: dict, type: str):
        match type:
            case EventType.ChatMessage:
                sub_type = data.get("message", {}).get("type")
                data = ChatMessage(data)
            case EventType.DeleteMessage:
                sub_type = None
                data = DeleteChatMessage(data)
            case _:
                sub_type = None
                data = BaseEvent(data, type)

        try:
            await self._run_middlewares(data, type, sub_type)
        except MiddlewareStopException:
            log.debug(f"[ws][middleware] Event {type} stopped by middleware")
            return

        if type in self.handlers or EventType.ANY in self.handlers or f"{type}:{sub_type}" in self.handlers:
            for i in (EventType.ANY, type, f"{type}:{sub_type}"):
                if i not in self.handlers:
                    continue
                for func in self.handlers[i]:
                    try:
                        await func(data)
                    except Exception as e:
                        log.error(f"[ws][event][{func}]Error: {e}")

    async def _run_middlewares(self, data, type: str, sub_type=None):
        middlewares_to_run = []

        if EventType.ANY in self.middlewares:
            middlewares_to_run.extend(self.middlewares[EventType.ANY])
        if type in self.middlewares:
            middlewares_to_run.extend(self.middlewares[type])
        if sub_type and f"{type}:{sub_type}" in self.middlewares:
            middlewares_to_run.extend(self.middlewares[f"{type}:{sub_type}"])

        for middleware in middlewares_to_run:
            try:
                result = await middleware(data)
                if result is False:
                    raise MiddlewareStopException()
            except MiddlewareStopException:
                raise
            except Exception as e:
                log.error(f"[ws][middleware][{middleware}]Error: {e}")

    def event(self, type: str | int):
        """Decorator to register an event handler"""
        def registerHandler(handler):
            self.add_handler(type, handler)
            return handler
        return registerHandler

    def add_handler(self, type: str | int, handler):
        """Registers an event handler for a specific event type"""
        if type in self.handlers:
            self.handlers[type].append(handler)
        else:
            self.handlers[type] = [handler]
        return handler

    def middleware(self, type: str | int = EventType.ANY):
        """Decorator to register a middleware"""
        def registerMiddleware(func):
            self.add_middleware(type, func)
            return func
        return registerMiddleware

    def add_middleware(self, type: str | int, middleware):
        """Registers a middleware for a specific event type"""
        if type not in self.middlewares:
            self.middlewares[type] = []
        self.middlewares[type].append(middleware)
        return middleware

    @staticmethod
    def command_validator(commands: list[str], handler):
        async def wrapped_handler(data: ChatMessage):
            if not isinstance(data.content, str):
                return
            message_content = data.content.lower()
            for command in commands:
                if message_content.startswith(command.lower()):
                    data.content = data.content[len(command):].strip()
                    await handler(data)
                    break
            return wrapped_handler
        return wrapped_handler

    def command(self, commands: list):
        """Decorator to register a command handler"""
        def registerCommands(handler):
            self.add_command(commands, handler)
            return handler
        return registerCommands

    def add_command(self, commands: list, handler):
        """Registers a command handler for messages"""
        if EventType.ChatTextMessage in self.handlers:
            self.handlers[EventType.ChatTextMessage].append(self.command_validator(commands, handler))
        else:
            self.handlers[EventType.ChatTextMessage] = [self.command_validator(commands, handler)]
        return self.command_validator

    def is_command(self, message: str) -> bool:
        """Checks if a message contains a registered command"""
        if not message or not isinstance(message, str):
            return False
        message = message.lower().strip()
        if EventType.ChatTextMessage not in self.handlers:
            return False
        for handler in self.handlers[EventType.ChatTextMessage]:
            if hasattr(handler, "__closure__") and handler.__closure__:
                for cell in handler.__closure__:
                    val = cell.cell_contents
                    if isinstance(val, list):
                        for command in val:
                            if message.startswith(command.lower()):
                                return True
        return False
