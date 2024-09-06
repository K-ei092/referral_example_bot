import random

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from configuration.config import load_config_bot
from lexicon.lexicon import LEXICON_kb


# Загружаем список админов
admins: list[int] = load_config_bot().tg_bot.admin_ids


# Загружаем список каналов
channals: list[str] = load_config_bot().tg_bot.channel_links


def main_kb(user_telegram_id: int):
    kb_list = [[KeyboardButton(text=LEXICON_kb['main_kb_user'])]]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=LEXICON_kb['main_kb_admin'])])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=LEXICON_kb['main_kb_placeholder']
    )


def admin_desk_kb():
    kb_builder = InlineKeyboardBuilder()
    button_text = InlineKeyboardButton(text=LEXICON_kb['admin_desk_kb_text'],
                                       callback_data='admin_deck^send_statistic_text')
    button_file = InlineKeyboardButton(text=LEXICON_kb['admin_desk_kb_file'],
                                       callback_data='admin_deck^send_statistic_file')
    button_raffle = InlineKeyboardButton(text=LEXICON_kb['admin_desk_kb_raffle'],
                                         callback_data='raffle_prize')
    buttons: list[InlineKeyboardButton] = [button_text, button_file, button_raffle]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


def confirm_action_kb():
    kb_builder = InlineKeyboardBuilder()
    button_confirm_action = InlineKeyboardButton(text=LEXICON_kb['confirm_action_kb_start'],
                                                 callback_data='confirm_action')
    button_stop_raffle = InlineKeyboardButton(text=LEXICON_kb['confirm_action_kb_stop'],
                                              callback_data='stop_raffle')
    buttons: list[InlineKeyboardButton] = [button_confirm_action, button_stop_raffle]
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


def channel_kb():
    kb_builder = InlineKeyboardBuilder()
    for channal in channals:
        kb_builder.row(InlineKeyboardButton(
            text=f'@{channal}',
            callback_data=f'{channal}'
        ))
    return kb_builder.as_markup()


def create_keyboard_captcha():

    correct_smile: str | None = None
    smiles: list = LEXICON_kb['smiles']
    callback_datas: list = LEXICON_kb['callback_datas']
    random.shuffle(callback_datas)

    data: dict[str, str] = dict(zip(smiles, callback_datas))

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for smile, callback_data in data.items():
        button = InlineKeyboardButton(text=smile, callback_data=callback_data)
        buttons.append(button)
        if callback_data == '^winner^':
            correct_smile = smile

    kb_builder.row(*buttons, width=7)
    return kb_builder.as_markup(), correct_smile


def home_page_kb(user_telegram_id: int):
    kb_list = [[KeyboardButton(text=LEXICON_kb['home_page_kb_user'])]]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=LEXICON_kb['home_page_kb_admin'])])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=LEXICON_kb['home_page_kb_placeholder']
    )


def like_kb(count: int = 0):
    kb_builder = InlineKeyboardBuilder()
    button_text = InlineKeyboardButton(text=LEXICON_kb['like_kb'].format(count=count), callback_data='like_raffle')
    buttons: list[InlineKeyboardButton] = [button_text]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()
