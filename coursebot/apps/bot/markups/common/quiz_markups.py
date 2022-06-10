from aiogram.utils.keyboard import InlineKeyboardBuilder


def quiz(a: str, b: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=a, callback_data=a)
    builder.button(text=b, callback_data=b)
    builder.adjust(2)
    return builder.as_markup()
