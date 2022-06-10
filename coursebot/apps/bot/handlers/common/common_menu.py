from aiogram import Dispatcher, Router, types, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from loguru import logger

from coursebot.apps.bot.callback_data.base_callback import CourseCallback
from coursebot.apps.bot.filters.base_filters import UserFilter
from coursebot.apps.bot.markups.common import common_markups
from coursebot.db.models import User, Course

router = Router()


class SignUpCourse(StatesGroup):
    language = State()
    level = State()


async def start(message: types.Message | types.CallbackQuery, user: User, is_new: bool, state: FSMContext):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message

    # Для новых пользователей
    if is_new or not user.registered_user:
        await message.answer("Приветственное сообщение!", reply_markup=common_markups.new_user_start_menu())

    else:
        await message.answer("Приветственное сообщение!", reply_markup=common_markups.start_menu())


async def about_course(message: types.Message):
    await message.answer("Информация о курсах")


async def about_company(message: types.Message):
    await message.answer("Информация о компании")


async def my_courses(message: types.Message, user: User):
    courses = await user.registered_user.courses
    courses_view = ""
    for num, c in enumerate(courses):
        courses_view += f"#{num}. {c.title}\n"
    await message.answer(f"Вы записаны на курс(ы):\n{courses_view}")


async def signup_for_course(message: types.Message, state: FSMContext):
    await message.answer("Выберите язык, который вы хотели бы изучить",
                         reply_markup=common_markups.signup_for_course())
    await state.set_state(SignUpCourse.language)


async def signup_for_course_language(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(title=call.data)
    logger.info(call)
    await call.message.answer("Выберите уровень ваших знаний данного языка",
                              reply_markup=common_markups.signup_for_course_language())
    await state.set_state(SignUpCourse.level)


async def signup_for_course_level(call: types.CallbackQuery, user: User, state: FSMContext):
    await state.update_data(level=call.data)
    await user.fetch_related("registered_user")
    data = await state.get_data()
    await Course.create(**data, registered_user=user.registered_user)
    await call.message.answer("Вы успешно записались на курс")
    await state.clear()


async def unsubscribe_from_course(message: types.Message, user: User, state: FSMContext):
    await user.fetch_related("registered_user__courses")
    courses = user.registered_user.courses
    logger.info(courses)
    await message.answer("На какой курс хотите отменить запись",
                         reply_markup=common_markups.unsubscribe_from_course(courses))


async def unsubscribe_from_course_delete(call: types.CallbackQuery, callback_data: CourseCallback, ):
    course = await Course.get(pk=callback_data.pk)
    await course.delete()
    await call.message.answer(f"Вы успешно отписались от курса {course.title}")


def register_common(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(start, UserFilter(), commands="start", state="*")
    callback(start, UserFilter(), text="start", state="*")

    message(about_course, text="Узнать о курсах", state="*")
    message(about_company, text="Узнать о компании", state="*")
    message(my_courses, UserFilter(), text="Мои курсы", state="*")

    message(signup_for_course, text="Записаться на курс", state="*")
    callback(signup_for_course_language, state=SignUpCourse.language)
    callback(signup_for_course_level, UserFilter(), state=SignUpCourse.level)

    message(unsubscribe_from_course, UserFilter(), text="Отменить запись на курс", state="*")
    callback(unsubscribe_from_course_delete, CourseCallback.filter(F.action == "delete"))
