from aiogram.fsm.state import State, StatesGroup


# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# для группы состояний FSM капчи
class FSMFillForm(StatesGroup):
    fill_captcha = State()          # Состояние ожидания решения каптчи


# для группы состояний FSM розыгрыша
class FSMFillRaffle(StatesGroup):
    fill_channel = State()          # Состояние ожидания выбора канала админом в котором проведем розыгрыш
    fill_count_referral = State()    # Состояние ожидания введения условий проведения розыгрыша
    fill_confirm_action = State()   # Состояние ожидания подтверждения начала розыгрыша
    fill_participants = State()     # Состояние определения участников
    fill_count_like = State()       # Состояние ожидания лайков
    fill_users_like = State()       # Состояние для хранения юзеров кто лайкнул пост
