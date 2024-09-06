import asyncio

from aiogram import Router, F, Bot

from aiogram.filters import CommandStart, CommandObject, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.utils.chat_action import ChatActionSender

from configuration.config import load_config_bot
from filters.filters import IsPrivatChat

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.table_processing import (
    get_user_data,
    insert_user,
    change_chat_member_counter,
    change_count_refer
)
from fsm.fsm_mode import FSMFillForm
from lexicon.lexicon import LEXICON, LEXICON_USER

from utils.utils import get_refer_id

from keyboards.kb import main_kb, create_keyboard_captcha


router = Router()


# Загружаем список каналов
channel_links: list[str] = load_config_bot().tg_bot.channel_links

# загружаем ссылку на бот
bot_link: str = load_config_bot().tg_bot.bot_link


# Хэндлер на команду "/restart"
@router.message(Command(commands='restart'), IsPrivatChat())
async def process_restart_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON[message.text])


# Хэндлер на команду "/start"
@router.message(CommandStart(), StateFilter(default_state), IsPrivatChat())
async def process_start_command(message: Message, state: FSMContext, command: CommandObject):
    my_keyboard, antibot_test = create_keyboard_captcha()
    await message.answer(text=LEXICON_USER['start_command_hd'].format(antibot_test=antibot_test),
                         reply_markup=my_keyboard)
    await state.set_state(FSMFillForm.fill_captcha)
    refer_id = get_refer_id(command.args)
    await state.update_data(fill_captcha=refer_id)


# Хэндлер сработает на пройденную капчу
@router.callback_query(F.data == '^winner^')
async def process_win_captcha(callback: CallbackQuery, db_engine: AsyncEngine, state: FSMContext):
    await asyncio.sleep(1)
    await callback.message.delete()
    user_info = await get_user_data(user_id=callback.from_user.id, db_engine=db_engine)
    if user_info:
        response_text = LEXICON_USER['win_captcha_hd_1'].format(
            full_name=user_info.get("full_name"),
            universe_text=LEXICON_USER['universe_text'])
        for link in channel_links:
            response_text += f'{LEXICON["full_link"].format(link=link)}\n'
    else:
        refer_id = (await state.get_data())['fill_captcha']
        # await state.clear()

        user_data = {
            'user_id': callback.from_user.id,
            'full_name': callback.from_user.full_name,
            'user_login': callback.from_user.username,
            'refer_id': refer_id,
            'count_refer': 0,
            'chat_member_counter': 0    # ставим 0 - False, при подписке увеличение / при отписке уменьшение на 1 - True
        }
        await insert_user(user_data=user_data, db_engine=db_engine)

        if refer_id:
            response_text = LEXICON_USER['win_captcha_hd_2'].format(full_name=user_data["full_name"], refer_id=refer_id)
        else:
            response_text = LEXICON_USER['win_captcha_hd_3'].format(full_name=user_data["full_name"])

        response_text += LEXICON_USER['win_captcha_hd_4']

        for link in channel_links:
            response_text += f'{LEXICON["full_link"].format(link=link)}\n'

        response_text += f'\n{LEXICON_USER["universe_text"]}'

    await callback.message.answer(text=response_text,
                                  reply_markup=main_kb(callback.from_user.id),
                                  disable_web_page_preview=True)
    await state.clear()


# Хэндлер сработает на проваленную капчу
@router.callback_query(F.data.startswith('^losser^'))
async def process_los_captcha(callback: CallbackQuery):
    msg = await callback.message.answer(text=LEXICON_USER['los_captcha_hd'])
    await asyncio.sleep(1.5)
    await msg.delete()


# Хэндлер на команду "/help"
@router.message(Command(commands='help'), IsPrivatChat())
async def process_help_command(message: Message):
    msg = await message.answer(text=LEXICON[message.text])
    await asyncio.sleep(35)
    await msg.delete()


# Хэндлер на появление нового пользователя в канале
@router.chat_member(F.chat.type == 'channel', ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_channel(event: ChatMemberUpdated, db_engine: AsyncEngine, bot: Bot):
    user_id = event.from_user.id
    user_info = await get_user_data(user_id=user_id, db_engine=db_engine)
    if user_info and not event.from_user.is_bot:
        refer_id = user_info['refer_id']
        user_login = f'ID: <code><b>{user_id}</b></code>' if not user_info['user_login'] else f'@{user_info["user_login"]}'
        chat_member_counter = user_info['chat_member_counter']
        await change_chat_member_counter(user_id, db_engine, plus=True)
        if (chat_member_counter == 0) and refer_id:
            await change_count_refer(refer_id, db_engine, plus=True)
            await bot.send_message(
                chat_id=refer_id,
                text=LEXICON_USER['new_member_hd'].format(user_login=user_login, event_chat_title=event.chat.title),
                request_timeout=30
            )


# Хэндлер на выход пользователя из канала
@router.chat_member(F.chat.type == 'channel', ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> IS_NOT_MEMBER))
async def left_member_channel(event: ChatMemberUpdated, db_engine: AsyncEngine, bot: Bot):
    user_id = event.from_user.id
    user_info = await get_user_data(user_id=user_id, db_engine=db_engine)
    if user_info and not event.from_user.is_bot:
        refer_id = user_info['refer_id']
        user_login = f'ID: <code><b>{user_id}</b></code>' if not user_info['user_login'] else f'@{user_info["user_login"]}'
        chat_member_counter = user_info['chat_member_counter']
        await change_chat_member_counter(user_id, db_engine, plus=False)
        if (chat_member_counter == 1) and refer_id:
            await change_count_refer(refer_id, db_engine, plus=False)
            await bot.send_message(
                chat_id=refer_id,
                text=LEXICON_USER['left_member_hd'].format(user_login=user_login),
                request_timeout=30
            )
    else:
        user_data = {
            'user_id': event.from_user.id,
            'full_name': event.from_user.full_name,
            'user_login': event.from_user.username,
            'refer_id': None,
            'count_refer': 0,
            'chat_member_counter': -1
        }
        await insert_user(user_data=user_data, db_engine=db_engine)


# Хэндлер на появление нового пользователя в чате
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_group(event: ChatMemberUpdated, db_engine: AsyncEngine, bot: Bot):
    user_id = event.from_user.id
    user_info = await get_user_data(user_id=user_id, db_engine=db_engine)
    if user_info and not event.from_user.is_bot:
        refer_id = user_info['refer_id']
        user_login = f'ID: <code><b>{user_id}</b></code>' if not user_info['user_login'] else f'@{user_info["user_login"]}'
        chat_member_counter = user_info['chat_member_counter']
        await change_chat_member_counter(user_id, db_engine, plus=True)
        if (chat_member_counter == 0) and refer_id:
            await change_count_refer(refer_id, db_engine, plus=True)
            await bot.send_message(
                chat_id=refer_id,
                text=LEXICON_USER['new_member_hd'].format(user_login=user_login, event_chat_title=event.chat.title),
                request_timeout=30
            )


# Хэндлер на выход пользователя из чата
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> IS_NOT_MEMBER))
async def left_member_group(event: ChatMemberUpdated, db_engine: AsyncEngine, bot: Bot):
    user_id = event.from_user.id
    user_info = await get_user_data(user_id=user_id, db_engine=db_engine)
    if user_info and not event.from_user.is_bot:
        refer_id = user_info['refer_id']
        user_login = f'ID: <code><b>{user_id}</b></code>' if not user_info['user_login'] else f'@{user_info["user_login"]}'
        chat_member_counter = user_info['chat_member_counter']
        await change_chat_member_counter(user_id, db_engine, plus=False)
        if (chat_member_counter == 1) and refer_id:
            await change_count_refer(refer_id, db_engine, plus=False)
            await bot.send_message(
                chat_id=refer_id,
                text=LEXICON_USER['left_member_hd'].format(user_login=user_login),
                request_timeout=30
            )
    else:
        user_data = {
            'user_id': event.from_user.id,
            'full_name': event.from_user.full_name,
            'user_login': event.from_user.username,
            'refer_id': None,
            'count_refer': 0,
            'chat_member_counter': -1
        }
        await insert_user(user_data=user_data, db_engine=db_engine)


# хендлер на команду или кнопку вызова профиля
@router.message(Command('profile'), IsPrivatChat())
@router.message(F.text.contains('Мой профиль'))
async def get_profile(message: Message, db_engine: AsyncEngine, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id, db_engine=db_engine)
        if user_info:
            text = LEXICON_USER['get_profile_hd_1'].format(
                id_1=message.from_user.id,
                count_refer=user_info.get("count_refer"),
                bot_link=bot_link,
                id_2=message.from_user.id
            )
            await message.answer(text)
        else:
            await message.answer(text=LEXICON_USER['get_profile_hd_2'])
