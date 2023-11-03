from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Допомога')],
        [KeyboardButton(text='Вихід')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)