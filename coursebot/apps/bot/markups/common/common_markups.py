from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from loguru import logger

from coursebot.apps.bot.callback_data.base_callback import CourseCallback
from coursebot.db.models import Course


def new_user_start_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Я новый клиент", callback_data="new_user")
    builder.button(text="Я уже занимаюсь на курсах", callback_data="exist_user")
    builder.adjust(1)
    return builder.as_markup()


def start_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Узнать о курсах")
    builder.button(text="Узнать о компании")
    builder.button(text="Мои курсы")
    builder.button(text="Викторина")
    builder.button(text="Записаться на курс")
    builder.button(text="Отменить запись на курс")
    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True)


def signup_for_course():
    # keyboard = [
    #     ('Английский', "Английский"),
    #     ('Французский', "Французский"),
    #     ('Испанский', "Испанский"),
    #     ('Немецкий', "Немецкий"),
    #     ('Китайский', "Китайский")
    # ]
    keyboard = [
        'Английский',
        'Французский',
        'Испанский',
        'Немецкий',
        'Китайский',
    ]
    builder = InlineKeyboardBuilder()

    for i in keyboard:
        builder.button(text=i, callback_data=i)
    builder.adjust(1)

    return builder.as_markup()


def signup_for_course_language():
    keyboard = [
        'Начальный',
        'Средний',
        'Продвинутый',
    ]
    builder = InlineKeyboardBuilder()
    for i in keyboard:
        builder.button(text=i, callback_data=i)
    builder.adjust(1)
    logger.info(builder)
    return builder.as_markup()


def unsubscribe_from_course(courses: list[Course]):
    builder = InlineKeyboardBuilder()
    for c in courses:
        builder.button(text=c.title, callback_data=CourseCallback(pk=c.pk, action="delete"))
    builder.adjust(1)
    return builder.as_markup()
