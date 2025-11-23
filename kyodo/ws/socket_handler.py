from ..utils import log
from traceback import format_exc
from ..objects import EventType, ChatMessage, BaseEvent

class MiddlewareStopException(Exception):
    """Исключение для остановки цепи обработчиков"""
    pass

class Handler:
    """ Additional module to socket for creating event handlers """
    handlers: dict = {}
    middlewares: dict = {}
    error_trace: bool

    async def handle_data(self, _data: dict):
        data: dict = _data.get("d", {})
        _o = _data.get("o")
        await self.call(data, _o)

    async def call(self, data: dict, type: str):
        match type:
            case EventType.ChatMessage:
                sub_type = data.get("message", {}).get("type")
                data = ChatMessage(data)
            case _:
                sub_type = None
                data = BaseEvent(data, type)

        # Запускаем middleware перед обработчиками
        try:
            await self._run_middlewares(data, type, sub_type)
        except MiddlewareStopException:
            log.debug(f"[ws][middleware] Обработка события {type} остановлена middleware")
            return

        if type in self.handlers or EventType.ANY in self.handlers or f"{type}:{sub_type}" in self.handlers:
            for i in (EventType.ANY, type, f"{type}:{sub_type}"):
                if i not in self.handlers:
                    continue
                for func in self.handlers[i]:
                    try:
                        await func(data)
                    except Exception as e:
                        log.error(f"[ws][event][{func}]Error: {e}{'' if not self.error_trace else f'\n{format_exc()}'}")

    async def _run_middlewares(self, data, type: str, sub_type=None):
        """Запускает middleware для данного типа события"""
        middlewares_to_run = []

        # Собираем все применимые middleware
        if EventType.ANY in self.middlewares:
            middlewares_to_run.extend(self.middlewares[EventType.ANY])
        if type in self.middlewares:
            middlewares_to_run.extend(self.middlewares[type])
        if sub_type and f"{type}:{sub_type}" in self.middlewares:
            middlewares_to_run.extend(self.middlewares[f"{type}:{sub_type}"])

        # Запускаем middleware по очереди
        for middleware in middlewares_to_run:
            try:
                result = await middleware(data)
                if result is False:  # Middleware вернул False - останавливаем цепь
                    raise MiddlewareStopException()
            except MiddlewareStopException:
                raise
            except Exception as e:
                log.error(f"[ws][middleware][{middleware}]Error: {e}{'' if not self.error_trace else f'\n{format_exc()}'}")

    def event(self, type: str | int):
        """ Decorator for registering an event handler. """
        def registerHandler(handler):
            self.add_handler(type, handler)
            return handler
        return registerHandler

    def add_handler(self, type: str | int, handler):
        """ Registers an event handler for a specific event type. """
        if type in self.handlers:
            self.handlers[type].append(handler)
        else:
            self.handlers[type] = [handler]
        return handler

    def middleware(self, type: str | int = EventType.ANY):
        """ Decorator for registering a middleware. """
        def registerMiddleware(func):
            self.add_middleware(type, func)
            return func
        return registerMiddleware

    def add_middleware(self, type: str | int, middleware):
        """ Registers a middleware for a specific event type. """
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
        """ Decorator for registering a command handler. """
        def registerCommands(handler):
            self.add_command(commands, handler)
            return handler
        return registerCommands

    def add_command(self, commands: list, handler):
        """ Registers a command handler for processing messages. """
        if EventType.ChatTextMessage in self.handlers:
            self.handlers[EventType.ChatTextMessage].append(self.command_validator(commands, handler))
        else:
            self.handlers[EventType.ChatTextMessage] = [self.command_validator(commands, handler)]
        return self.command_validator

    def is_command(self, message: str) -> bool:
        """ Проверяет, содержит ли сообщение одну из зарегистрированных команд. """
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