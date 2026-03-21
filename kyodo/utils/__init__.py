from .logger import Logger, logging
from .exceptions import NeedAuthError


log = Logger()

def require_auth(func):
    def wrapper(self, *args, **kwargs):
        if not getattr(self, "token", ""):
            raise NeedAuthError(
                "You need to be authorized to use this method"
            )
        return func(self, *args, **kwargs)

    return wrapper


def require_uid(func):
    def wrapper(self, *args, **kwargs):
        if not getattr(self.me, "userId", ""):
            raise NeedAuthError(
                "Your account ID is required. Login via token does not provide information about your ID. To specify your ID use: client.me.userId = 'your_id'"
            )
        return func(self, *args, **kwargs)

    return wrapper
