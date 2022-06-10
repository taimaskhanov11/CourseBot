from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def start_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Узнать о курсах")
    builder.button(text="Узнать о компании")
    builder.button(text="Мои Курсы")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
