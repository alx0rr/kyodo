from jwt import encode
from random import choices
from string import digits, ascii_letters
from datetime import datetime, timezone, timedelta
from time import time
from orjson import dumps
from hashlib import sha256

from base64 import b64encode

def random_ascii_string(length=11) -> str:
    """
    Generates a random ASCII string.

    Args:
        length (int): Length of the generated string. Default is 11.

    Returns:
        str: Randomly generated ASCII string.
    """
    return ''.join(choices(digits+ascii_letters, k=length))


def get_utc_time() -> str:
    """
    Returns the current UTC time in ISO 8601 format.

    Returns:
        str: Current time in UTC with millisecond precision and 'Z' suffix.
    """
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def get_target_date(days_from_now: int) -> str:
    """
    Returns the date after a specified number of days.

    Args:
        days_from_now (int): Number of days from the current date.

    Returns:
        str: Target date in "Day Mon DD YYYY HH:MM:SS GMT+0200" format.
    """
    target = datetime.now() + timedelta(days=days_from_now)
    return target.strftime('%a %b %d %Y %H:%M:%S GMT+0200')



def date_string_to_timestamp_ms(date: str) -> int:
    """
    Converts a date string in the format "DD.MM.YYYY" to a Unix timestamp in milliseconds.

    Args:
        date (str): The date string in the format "day.month.year" (e.g., "12.04.2003").

    Returns:
        int: The corresponding Unix timestamp in milliseconds since 01.01.1970 UTC.
    """
    dt = datetime.strptime(date, "%d.%m.%Y")
    return int(dt.timestamp() * 1000)


def strtime() -> str:
    return str(int(time() * 1000))


def _x_signature(secret: str, _time: int) -> str:
    return encode(
        {"typeof": "xSig", "exp": _time}, secret, algorithm="HS256"
    )


def _x_sig(device_id: str, uid: str, reqtime: str, body: dict | bytes) -> str:
    if isinstance(body, dict):data = dumps(body).decode("utf-8")
    elif isinstance(body, bytes):data ="{}" # idk/ TODO
    else:data = "{}"
    return sha256(
        dumps(
            {
                "startTime": reqtime,
                "uid": uid,
                "deviceId": device_id,
                "data": data,
            }
        )
    ).hexdigest()
