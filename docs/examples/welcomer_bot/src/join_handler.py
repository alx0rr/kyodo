_ = 0
from . import client
from .utils import download_image, create_greeting_image
from kyodo import EventType, ChatMessage, ChatType, log
from aiofiles import open


@client.event(EventType.ChatMemberJoin)
async def on_member_join(message: ChatMessage):
    chat = await client.get_chat_info(message.circleId, message.chatId)
    if chat.type == ChatType.PRIVATE: return
    log.info(f"New member: {message.author.nickname}")
    
    if message.author.avatar:
        avatar = await download_image(message.author.avatar, f"avatar_{message.author.userId}")
    else: avatar =  "base_avatar.png"
    result = await create_greeting_image(
        message.author.nickname or f"@{message.author.handle}",
        chat.name, chat.memberCount, avatar, f"cache/greeting_{message.author.userId}.png", "background.png")
    
    async with open(result, "rb") as file:
        await client.send_photo(message.circleId, message.chatId, file)



