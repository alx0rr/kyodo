from . import client
from kyodo import log
from config import email, password, auth_token

async def auth():
    if auth_token:
        try:
            await client.login_token(auth_token)
            log.info(f"Login as {client.me.nickname}")
            return
        except Exception as e:
            log.error(f"Failed to log in using token: {e}")
    
    if email and password:
        try:
            await client.login(email, password)
            log.info(f"Login as {client.me.nickname}")
            return
        except Exception as e:
            log.error(f"Failed to log in using email: {e}")
    
    log.critical("Failed to login.")
    return False
    