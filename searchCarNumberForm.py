from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from router import form_router
from buttons import getMainButtons
from models.User import User
from stringUtils import transformCarNumber


class SearchCarNumberForm(StatesGroup):
    check_car_number = State()

@form_router.message(F.text.lower() == "проверить номер машины")
async def search_by_car_number(message: Message, state: FSMContext):
    await state.set_state(SearchCarNumberForm.check_car_number)
    await message.answer("Введите номер машины", reply_markup=ReplyKeyboardRemove())

@form_router.message(SearchCarNumberForm.check_car_number)
async def process_car_number(message: Message, state: FSMContext):
    car_number = transformCarNumber(message.text)
    users = []
    # получение юзеров из БД по car_number
    user = None
    if len(users) > 0:
        user = users[0]
    await state.clear()
    buttons = getMainButtons(message.from_user.id)
    kb = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    if user is None:
        await message.answer(text="Машины нет в списке", reply_markup=kb)
    else:
        await message.answer(text="Машина найдена", reply_markup=kb)
        text = (f"{user.last_name} {user.first_name} {user.middle_name}, "
                f"тел. {user.phone}")
        for car in user.cars:
            text += f", авто {car.number}"
        await message.answer(text=text)

