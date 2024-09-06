from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivatChat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type == 'private':
            return True
        else:
            return False
