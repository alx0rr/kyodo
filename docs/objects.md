# Objects

In Kyodo, objects are divided into two categories:

1. **Function argument objects** — used to pass constants into methods, avoiding magic numbers or strings.  
2. **Response objects** — structured objects returned by functions or available in events for convenient data access.

You can view all objects in the following folders:

- [objects](https://github.com/alx0rr/kyodo/tree/main/kyodo/objects) - objects returned from functions
- [args](https://github.com/alx0rr/kyodo/tree/main/kyodo/objects/args) - objects for function arguments and comparisons


---
### Import:

```python
from kyodo import ChatType, ChatMessage, ChatReplyMessage
#or 
from kyodo import args
args.ChatType
```

---

## 🔹 Function Argument Objects

These objects make function calls safer and more readable:

```python
# Chat type
args.ChatType.PRIVATE
args.ChatType.GROUP
args.ChatType.PUBLIC

# Message type
args.ChatMessageTypes.Text
args.ChatMessageTypes.Photo
args.ChatMessageTypes.Video
args.ChatMessageTypes.Sticker
```

Using these objects prevents mistakes caused by passing raw numbers or strings.

---

## 🔹 Response Objects

Response objects are returned by library methods or available in event handlers.  
They allow convenient access to data through attributes instead of raw dictionaries.

Example in an event handler:

```python
async def hello_handler(message: ChatMessage):
    # Access reply message content
    print(message.replyMessage.content)

    # Access author information
    author = message.replyMessage.author
    print(author.nickname)

    # Access message ID
    print(message.replyMessage.messageId)
```

Example structure of a response object (`ChatReplyMessage`):

```python
class ChatReplyMessage:
	def __init__(self, data: dict):
		data = data or {}

		self.data = data
		self.messageId: str = data.get("id")
		self.userId: str = data.get("user", {}).get("uid")

		self.content: str = data.get("content")
		self.type: int = data.get("type")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")

		self.author: UserProfile = UserProfile(data.get("user", {}))

		self.sticker: StickerInfo = StickerInfo(data.get("sticker", {}))
```

**Key points:**
- Objects can have **nested structures** (`author`, `replyMessage`)  
- Fields are accessed directly via **attributes**, no need to parse raw dictionaries  
- Ideal for use in **async event handlers**

---

## 🔗 Navigation

[⬅️ Main page](index.md) | [Next section: Logging Configuration](logging.md)
