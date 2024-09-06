LEXICON: dict[str, str] | dict[str, list[str]] = {
    '/help': 'Реферал засчитывается, если он подписался на канал(ы). Вам поступит уведомление о его подписке. '
             'Также уведомление придет, если реферал отпишется от каналов. Засчитываются только новые '
             'подписчики.\n\nЕсли в процессе решения капчи проблемы, нажмите /restart.',
    '/restart': 'Запустите бот заново /start',
    'other_hd': 'Мне неизвестна команда "{message}"\nПопробуйте набрать /restart, /start или /help',
    'full_link': 'https://t.me/{link}'
}


LEXICON_ADMIN: dict[str, str] | dict[str, list[str]] = {
    'admin_deck': '📊 Выберите в каком формате представить статистику\n🎲 или начните розыгрыш',
    'statistic_text_1': '👥 В базе данных <b>{count}</b> человек(а). Кратко по каждому:\n\n',
    'statistic_text_2': '📝 Полное имя: {full_name}\n',
    'statistic_text_3': '🔑 Логин: @{user_login}\n',
    'statistic_text_4': '👥 Вовлёк: {count_refer}\n〰️〰️〰️〰️〰️〰️〰️〰️〰️\n',
    'statistic_file_1': 'Формирую базу{i}',
    'statistic_file_2': 'Готово',
    '....': ['.', '..', '...', '.', '..']
}


LEXICON_RAFFLE: dict[str, str] | dict[str, list[str]] = {
    'channel_hd': 'В каком канале разыграть?',
    'count_referral_hd': 'Отправьте мне сообщение с условием для проведения розыгрыша — минимальное количество '
                        'приведённых подписчиков, например: 2',
    'confirm_action_hd': 'Подтвердите старт розыгрыша.\nУсловия:\nпроводится в канале: {channel}\nУчаствуют '
                         'пользователи, которые привлекли не менее {count_referral} человек',
    'confirm_action_hd_not_user': 'Не найдено пользователей, которые привлекли не менее {count_referral} '
                                  'подписчика(ов)\nНастройте розыгрыш заново',
    'confirm_action_hd_error': 'Ошибка ввода данных! Попробуй ввести число заново',
    'raffle_to_be_hd': 'Объявляется розыгрыш 🥳🥳🥳\nУсловия для участия: подписать {count_referral} человек(а).\n'
                       'Эти условия выполнены следующими пользователями:\n',
    'to_be_&_count_like': 'Бот случайным образом 🎲 выберет победителя, когда этот пост наберет {like} реакций\n',
    'count_like_hd': 'Мы набрали лайки, и через минуту бот определит победителя 🤩',
    'count_like_hd_clocks': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛', '🕐', '🕑'],
    'count_like_hd_CLOCK': '🕛',
    'count_like_hd_winner': 'Победителем стал пользователь {winner} 🎊\nС чем его от всей души и поздравляем 🎉🎉🎉',
    'stop_hd': 'Процесс остановлен, настройки сброшены'
}


LEXICON_USER: dict[str, str] | dict[str, list[str]] = {
    'universe_text': 'Вы можете получить информацию о своем профиле, нажав на кнопку "Мой профиль", или '
                     'воспользовавшись специальной командой из меню. В профиле есть персональная ссылка для приглашения '
                     'подписчиков.',
    'start_command_hd': 'Пройдите проверку и нажмите на такой же смайл {antibot_test}',
    'win_captcha_hd_1': '{full_name}, вижу, что вы уже в моей базе данных.'
                      '\n\n{universe_text}\n\nКанал(ы) для подписок:\n',
    'win_captcha_hd_2': '{full_name}, вы добавлены в базу бота и закреплены за пользователем с ID <b>{refer_id}</b>.',
    'win_captcha_hd_3': '{full_name}, вы добавлены в базу бота и ни за кем не закреплены.',
    'win_captcha_hd_4': '\n\nЧтобы завершить регистрацию, подпишитесь на канал(ы):\n\n',
    'los_captcha_hd': 'Неверно, попробуй еще',
    'new_member_hd': 'Ваш реферал {user_login} подписался на: {event_chat_title}',
    'left_member_hd': 'Ваш реферал {user_login} отписался от всех каналов',
    'get_profile_hd_1': '🆔 Ваш телеграм ID: <code><b>{id_1}</b></code>\n👥 Количество привлеченных пользователей: '
                      '<b>{count_refer}</b>\n\n📌 Персональная ссылка для приглашения:\n🔗 '
                      'https://t.me/{bot_link}?start={id_2}',
    'get_profile_hd_2': 'У меня нет вашего профиля, попробуйте начать с команды /start'
}


LEXICON_kb: dict[str, str | list] = {
    'main_kb_user': '👤 Мой профиль',
    'main_kb_admin': '⚙️Панель администратора',
    'main_kb_placeholder': 'Воспользуйтесь меню:',
    'admin_desk_kb_text': '📄 Текст',
    'admin_desk_kb_file': '🗃 Файл',
    'admin_desk_kb_raffle': '⚙ Настроить розыгрыш',
    'confirm_action_kb_start': '🎲 Запустить',
    'confirm_action_kb_stop': '⛔ Отмена',
    'smiles': ['🙃', '😎', '😍', '😉', '🌹', '❤', '🤟'],
    'callback_datas': ['^losser^_1', '^losser^_2', '^losser^_3', '^losser^_4', '^losser^_5', '^losser^_6', '^winner^'],
    'home_page_kb_user': '🔙 Назад',
    'home_page_kb_admin': '⚙️Панель администратора',
    'home_page_kb_placeholder': 'Воспользуйтесь меню:',
    'like_kb': '{count} 🔥'
}


LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Запуск бота',
    '/profile': 'Мой профиль',
    '/help': 'Помощь',
    '/restart': 'Если проблемы с капчей'
}
