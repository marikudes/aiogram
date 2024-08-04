from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

startup_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пройти анкету"),
            KeyboardButton(text="Хочу рассказать о новости/проблеме")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да", callback_data = '/start'),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
