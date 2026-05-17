
from kyodo.objects import EventType, ChatMessage
from typing import Callable


class Router:
    def __init__(self):
        self.handlers: dict = {}
        self.middlewares: dict = {}

    def add_router(self, router: "Router"):
        """Merge a router's handlers and middlewares into this one"""
        for type_, funcs in router.handlers.items():
            if type_ in self.handlers:
                self.handlers[type_].extend(funcs)
            else:
                self.handlers[type_] = list(funcs)

        for type_, funcs in router.middlewares.items():
            if type_ in self.middlewares:
                self.middlewares[type_].extend(funcs)
            else:
                self.middlewares[type_] = list(funcs)

    def add_routers(self, *routers: "Router"):
        for router in routers:
            self.add_router(router)

    def event(self, type: str | int = EventType.ChatTextMessage):
        """Decorator to register an event handler"""
        def registerHandler(handler: Callable):
            self.add_handler(type, handler)
            return handler
        return registerHandler

    def add_handler(self, type: str | int, handler: Callable):
        """Registers an event handler for a specific event type"""
        if type in self.handlers:
            self.handlers[type].append(handler)
        else:
            self.handlers[type] = [handler]
        return handler

    def middleware(self, type: str | int = EventType.ANY):
        """Decorator to register a middleware"""
        def registerMiddleware(func: Callable):
            self.add_middleware(type, func)
            return func
        return registerMiddleware

    def add_middleware(self, type: str | int, middleware: Callable):
        """Registers a middleware for a specific event type"""
        if type not in self.middlewares:
            self.middlewares[type] = []
        self.middlewares[type].append(middleware)
        return middleware

    def command(self, commands: list):
        """Decorator to register a command handler"""
        def registerCommands(handler: Callable):
            self.add_command(commands, handler)
            return handler
        return registerCommands

    def add_command(self, commands: list, handler: Callable):
        """Registers a command handler for messages"""
        wrapped = self.command_validator(commands, handler)
        if EventType.ChatTextMessage in self.handlers:
            self.handlers[EventType.ChatTextMessage].append(wrapped)
        else:
            self.handlers[EventType.ChatTextMessage] = [wrapped]
        return wrapped

    @staticmethod
    def command_validator(commands: list[str], handler: Callable):
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

    def is_command(self, message: str) -> bool:
        if not message or not isinstance(message, str):
            return False
        message = message.lower().strip()
        if EventType.ChatTextMessage not in self.handlers:
            return False
        for handler in self.handlers[EventType.ChatTextMessage]:
            if hasattr(handler, "__closure__") and handler.__closure__:
                for cell in handler.__closure__:
                    try:
                        val = cell.cell_contents
                        if isinstance(val, list):
                            for command in val:
                                if message.startswith(command.lower()):
                                    return True
                    except ValueError:
                        pass
        return False