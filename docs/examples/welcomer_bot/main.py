from src.auth import auth
from src import client
from asyncio import run

async def main():
    if await auth() is not False:
        await client.socket_wait()

if __name__ == "__main__":
    run(main())
