class MiddlewareStopException(Exception):
    """Exception to stop the handler chain"""
    pass

from kyodo.ws.socket import Socket
