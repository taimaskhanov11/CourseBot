from aiogram import Dispatcher, Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from coursebot.apps.bot.markups.common import quiz_markups
from coursebot.config.config import MEDIA_DIR

router = Router()

quiz_photo_id: dict[int, str] = {}


def save_file_id(message: types.Message):
    quiz_photo_id[1] = message.photo[0].file_id


class Quiz(StatesGroup):
    quiz_1 = State()
    quiz_2 = State()
    quiz_3 = State()
    quiz_4 = State()
    quiz_5 = State()
    finish = State()


async def quiz_1(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(point=0)
    message = await message.answer_photo(quiz_photo_id.get(1, FSInputFile(MEDIA_DIR / "hare_1.png")),
                                         reply_markup=quiz_markups.quiz("Hair", "Hare"))
    save_file_id(message)
    await state.set_state(Quiz.quiz_2)


async def quiz_2(call: types.CallbackQuery, state: FSMContext):
    if call.data == "Hare":
        data = await state.get_data()
        data["point"] += 1
        await state.update_data(point=data["point"])

    message = await call.message.answer_photo(quiz_photo_id.get(2, FSInputFile(MEDIA_DIR / "sea_2.png")),
                                              reply_markup=quiz_markups.quiz("Sea", "See"))
    save_file_id(message)
    await state.set_state(Quiz.quiz_3)


async def quiz_3(call: types.CallbackQuery, state: FSMContext):
    if call.data == "Sea":
        data = await state.get_data()
        data["point"] += 1
        await state.update_data(point=data["point"])

    message = await call.message.answer_photo(quiz_photo_id.get(3, FSInputFile(MEDIA_DIR / "sun_3.png")),
                                              reply_markup=quiz_markups.quiz("Son", "Sun"))
    save_file_id(message)
    await state.set_state(Quiz.quiz_4)


async def quiz_4(call: types.CallbackQuery, state: FSMContext):
    if call.data == "Sun":
        data = await state.get_data()
        data["point"] += 1
        await state.update_data(point=data["point"])

    message = await call.message.answer_photo(quiz_photo_id.get(4, FSInputFile(MEDIA_DIR / "bee_4.png")),
                                              reply_markup=quiz_markups.quiz("Be", "Bee"))
    save_file_id(message)
    await state.set_state(Quiz.quiz_5)


async def quiz_5(call: types.CallbackQuery, state: FSMContext):
    if call.data == "Bee":
        data = await state.get_data()
        data["point"] += 1
        await state.update_data(point=data["point"])

    message = await call.message.answer_photo(quiz_photo_id.get(5, FSInputFile(MEDIA_DIR / "pear_5.png")),
                                              reply_markup=quiz_markups.quiz("Pair", "Pear"))
    save_file_id(message)
    await state.set_state(Quiz.finish)


async def quiz_finish(call: types.CallbackQuery, state: FSMContext):
    if call.data == "Pear":
        data = await state.get_data()
        data["point"] += 1
        await state.update_data(point=data["point"])
    data = await state.get_data()
    point = data['point']
    await call.message.answer(f"Ваш результат {point}/5")


def register_quiz(dp: Dispatcher):
    dp.include_router(router)

    callback = router.callback_query.register
    message = router.message.register

    message(quiz_1, text="Викторина", state="*")
    callback(quiz_2, state=Quiz.quiz_2)
    callback(quiz_3, state=Quiz.quiz_3)
    callback(quiz_4, state=Quiz.quiz_4)
    callback(quiz_5, state=Quiz.quiz_5)
    callback(quiz_finish, state=Quiz.finish)
