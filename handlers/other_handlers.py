from aiogram import Router
from aiogram.types import Message

from filters.filters import IsPrivatChat
from lexicon.lexicon import LEXICON

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(IsPrivatChat())
async def send_echo(message: Message):
    await message.answer(text=LEXICON['other_hd'].format(message=message.text))
