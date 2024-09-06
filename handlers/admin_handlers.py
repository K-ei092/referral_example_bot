import asyncio
import logging
import os

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from configuration.config import load_config_bot
from database.table_processing import get_all_users_data
from filters.filters import IsPrivatChat
from keyboards.kb import admin_desk_kb
from lexicon.lexicon import LEXICON_ADMIN
from utils.utils import get_statistic_file


router = Router()


logger = logging.getLogger(__name__)


# Загружаем список админов
admins: list[int] = load_config_bot().tg_bot.admin_ids


# хендлер для вызова админки
@router.message((F.text.endswith('Панель администратора')) & (F.from_user.id.in_(admins)), IsPrivatChat())
async def process_get_admin_deck(message: Message):
    my_keyboard = admin_desk_kb()
    await message.answer(
        text=LEXICON_ADMIN['admin_deck'],
        reply_markup=my_keyboard
    )


# хендлер, который отправляет статистику в текстовом сообщении или файлом
@router.callback_query(F.data.startswith('admin_deck'))
async def process_send_statistic(callback: CallbackQuery, bot: Bot, db_engine: AsyncEngine):
    async with ChatActionSender.typing(bot=bot, chat_id=callback.from_user.id):
        all_users_data = await get_all_users_data(db_engine)
        if 'send_statistic_text' in callback.data:
            admin_text = (
                LEXICON_ADMIN['statistic_text_1'].format(count=len(all_users_data))
            )
            for user in all_users_data:
                admin_text += LEXICON_ADMIN['statistic_text_2'].format(
                    full_name=user.get("full_name") if user.get("full_name") else user.get("user_id")
                )
                if user.get("user_login") is not None:
                    admin_text += LEXICON_ADMIN['statistic_text_3'].format(user_login=user.get("user_login"))
                admin_text += LEXICON_ADMIN['statistic_text_4'].format(count_refer=user.get("count_refer"))
            await callback.message.edit_text(admin_text)

        elif 'send_statistic_file' in callback.data:
            file_name = get_statistic_file(all_users_data)
            file = FSInputFile(file_name)
            for i in LEXICON_ADMIN['....']:
                await callback.message.edit_text(text=LEXICON_ADMIN['statistic_file_1'].format(i=i))
                await asyncio.sleep(0.2)
            await callback.message.edit_text(text=LEXICON_ADMIN['statistic_file_2'])
            await callback.message.answer_document(file)
            if os.path.isfile(file_name):
                os.remove(file_name)
