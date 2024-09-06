import asyncio
import pickle
import random

import redis

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncEngine

from configuration.config import load_config_bot
from database.table_processing import get_all_users_data
from fsm.fsm_mode import FSMFillRaffle

from keyboards.kb import channel_kb, confirm_action_kb, like_kb
from lexicon.lexicon import LEXICON_RAFFLE

router = Router()


# Загружаем список каналов
count_like_raffle: int = load_config_bot().tg_bot.count_like_raffle


# Выбор админом настройки розыгрыша
@router.callback_query(F.data == 'raffle_prize')
async def process_raffle_channel(callback: CallbackQuery, state: FSMContext):
    my_keyboard = channel_kb()
    await callback.message.edit_text(text=LEXICON_RAFFLE['channel_hd'], reply_markup=my_keyboard)
    await state.set_state(FSMFillRaffle.fill_channel)


# Перехватываем выбранный канал и запрашиваем условия розыгрыша (сколько привел подписчиков)
@router.callback_query(StateFilter(FSMFillRaffle.fill_channel))
async def process_raffle_count_referral(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.update_data(fill_channel=f'@{callback.data}')
    chat_id = callback.from_user.id
    await callback.message.delete()
    await bot.send_message(chat_id=chat_id, text=LEXICON_RAFFLE['count_referral_hd'])
    await state.set_state(FSMFillRaffle.fill_count_referral)


# Выбор админом условия розыгрыша
@router.message(StateFilter(FSMFillRaffle.fill_count_referral))
async def process_raffle_confirm_action(message: Message, state: FSMContext, db_engine: AsyncEngine):
    if message.text.isdigit():
        await state.update_data(fill_count_referral=message.text)
        channel = (await state.get_data()).get('fill_channel')
        count_referral: int = int((await state.get_data()).get('fill_count_referral'))
        all_users_data: list[dict] = await get_all_users_data(db_engine, count_referral)
        if all_users_data:
            my_keyboard = confirm_action_kb()
            await message.answer(
                text=LEXICON_RAFFLE['confirm_action_hd'].format(channel=channel, count_referral=count_referral),
                reply_markup=my_keyboard
            )
            await state.set_state(FSMFillRaffle.fill_confirm_action)
        else:
            await message.answer(
                text=LEXICON_RAFFLE['confirm_action_hd_not_user'].format(count_referral=count_referral)
            )
            await state.clear()
    else:
        await message.answer(text=LEXICON_RAFFLE['confirm_action_hd_error'])


# Перехват подтверждения розыгрыша и его проведение
@router.callback_query(StateFilter(FSMFillRaffle.fill_confirm_action), F.data == 'confirm_action')
async def process_raffle_to_be(callback: CallbackQuery, bot: Bot, state: FSMContext, db_engine: AsyncEngine):
    count_referral: int = int((await state.get_data()).get('fill_count_referral'))
    channel: str = (await state.get_data()).get('fill_channel')
    all_users_data: list[dict] = await get_all_users_data(db_engine, count_referral)
    participants = []
    text = LEXICON_RAFFLE['raffle_to_be_hd'].format(count_referral=count_referral)
    for user in all_users_data:
        participant = f'@{user.get("user_login")}' \
            if user.get("user_login") \
            else f"🆔 <code><b>{user.get('user_id')}</b></code>"
        participants.append(participant)
        text += f'{participant}, '
    text = text[:-2]

    # Сериализация списка в байты
    serialized_participants = pickle.dumps(participants)
    with redis.Redis(host='localhost', port=6379, db=14) as r:
        r.set(name='participant', value=serialized_participants)

    await callback.message.delete()
    await bot.send_message(chat_id=channel, text=text)
    my_keyboard = like_kb()
    await bot.send_message(chat_id=channel,
                           text=LEXICON_RAFFLE['to_be_&_count_like'].format(like=count_like_raffle),
                           reply_markup=my_keyboard)
    await state.clear()


# Подтверждение розыгрыша и его проведение
@router.callback_query(F.data == 'like_raffle')
async def process_raffle_count_like(callback: CallbackQuery, state: FSMContext):
    like_count = (await state.get_data()).get('fill_count_like') \
        if (await state.get_data()).get('fill_count_like') \
        else 0
    users_like = (await state.get_data()).get('fill_users_like') \
        if (await state.get_data()).get('fill_users_like') \
        else [callback.from_user.id]
    if len(users_like) == 1 or (callback.from_user.id not in users_like):
        like_count += 1
        my_keyboard = like_kb(like_count)
        await callback.message.edit_text(text=LEXICON_RAFFLE['to_be_&_count_like'].format(like=count_like_raffle),
                                         reply_markup=my_keyboard)
        await state.update_data(fill_count_like=like_count)
        users_like.append(callback.from_user.id)
        await state.update_data(fill_users_like=users_like)
    if like_count == count_like_raffle:
        await callback.message.edit_text(text=LEXICON_RAFFLE['count_like_hd'])
        with redis.Redis(host='localhost', port=6379, db=14) as r:
            serialized_participants = r.get('participant')
            r.delete('participant')
        # Десериализация обратно в исходный список
        participants = pickle.loads(serialized_participants)
        await state.clear()
        time_image = LEXICON_RAFFLE['count_like_hd_clocks']
        clb = await callback.message.answer(LEXICON_RAFFLE['count_like_hd_CLOCK'])
        for ti in time_image:
            try:
                await clb.edit_text(text=f'{ti}')
                await asyncio.sleep(1)
            except TelegramRetryAfter as e:
                retry_time = e.retry_after
                await asyncio.sleep(retry_time)
                break
        await asyncio.sleep(5)
        winner = random.choice(participants)
        await callback.message.answer(text=LEXICON_RAFFLE['count_like_hd_winner'].format(winner=winner))


# Выбор админом в каком канале проводится розыгрыш
@router.callback_query(F.data == 'stop_raffle')
async def process_raffle_stop(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RAFFLE['stop_hd'])
    await state.clear()
