from datetime import datetime

from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from loguru import logger

from coursebot.apps.bot.filters.base_filters import UserFilter
from coursebot.apps.bot.markups.common import common_markups
from coursebot.db.models import User, RegisteredUser

router = Router()


class Registration(StatesGroup):
    fio = State()
    date = State()
    phone = State()
    email = State()


class ExistUser(StatesGroup):
    fio = State()
    phone = State()


async def register_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите ваше ФИО")
    await state.set_state(Registration.fio)


async def register_fio(message: types.Message, state: FSMContext):
    try:
        first_name, last_name, patronymic = message.text.split()
        await state.update_data(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )
        await message.answer("Введите дату рождения в формате д.м.г\nНапример 15.02.1981")
        await state.set_state(Registration.date)
    except Exception as e:
        logger.warning(e)
        await message.answer("Неправильный ввод! Пример ввода: Иванов Иван Иванович")


# todo 6/10/2022 9:02 PM taima: проверить формат номера
async def register_date(message: types.Message, state: FSMContext):
    await state.update_data(birthdate=datetime.strptime(message.text, "%d.%m.%Y"))
    await message.answer("Введите ваш номер телефона")
    await state.set_state(Registration.phone)


async def register_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите ваш email")
    await state.set_state(Registration.email)


async def register_email(message: types.Message, user: User, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await RegisteredUser.create(**data, user=user)
    await message.answer("Вы успешно зарегистрировались!", reply_markup=common_markups.start_menu())


async def exist_user(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите ваше ФИО")
    await state.set_state(ExistUser.fio)


async def exist_user_fio(message: types.Message, state: FSMContext):
    try:
        first_name, last_name, patronymic = message.text.split()
        await state.update_data(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )
        await message.answer("Введите ваш номер телефона")
        await state.set_state(ExistUser.phone)
    except Exception as e:
        logger.warning(e)
        await message.answer("Неправильный ввод! Пример ввода: Иванов Иван Иванович")


async def exist_user_phone(message: types.Message, user: User, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    registered_user = await RegisteredUser.get_or_none(**data)
    if registered_user:
        registered_user.user = user
        await registered_user.save()
        await message.answer("Отлично! Можете узнать интересующую вас информацию, нажав на кнопки ниже",
                             reply_markup=common_markups.start_menu())
    else:
        await message.answer("К сожалению, я не могу вас найти в системе. Проверьте корректность введенных данных.",
                             reply_markup=common_markups.new_user_start_menu())


def register_registration(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register
    callback(register_start, text="new_user", state="*")
    message(register_fio, state=Registration.fio)
    message(register_date, state=Registration.date)
    message(register_phone, state=Registration.phone)
    message(register_email, UserFilter(), state=Registration.email)

    callback(exist_user, text="exist_user", state="*")
    message(exist_user_fio, state=ExistUser.fio)
    message(exist_user_phone, UserFilter(), state=ExistUser.phone)
