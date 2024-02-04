from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from router import form_router
from buttons import getMainButtons
from models.User import User
from stringUtils import transformCarNumber

import sqlite3


class SearchCarNumberForm(StatesGroup):
    check_car_number = State()

@form_router.message(F.text.lower() == "проверить номер машины")
async def search_by_car_number(message: Message, state: FSMContext):
    await state.set_state(SearchCarNumberForm.check_car_number)
    await message.answer("Введите номер машины", reply_markup=ReplyKeyboardRemove())

@form_router.message(SearchCarNumberForm.check_car_number)
async def process_car_number(message: Message, state: FSMContext):
    car_number = transformCarNumber(message.text)
    con = sqlite3.connect('parking_DB.sqlite3')
    cur = con.cursor()
    users = cur.execute('''SELECT * FROM cars WHERE chat_id = ? AND car = ?''',
                        (message.from_user.id, car_number)).fetchall()
    user_data = cur.execute('''SELECT * FROM usersdata WHERE chat_id = ?''', (message.from_user.id,)).fetchall()
    con.close()
    # получение юзеров из БД по car_number
    user = None
    if len(users) > 0:
        user = users[0]
        car_num = user[2]
        if user[3] == 'None':
            comment = 'Нет комментария'
        else:
            comment = user[3]
        fio, phone = str(user_data[0][2]), str(user_data[0][3])
        user = {'fio': fio, 'phone': phone, 'car': car_num, 'comment': comment}
    await state.clear()
    buttons = getMainButtons(message.from_user.id)
    kb = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    if user is None:
        await message.answer(text="Машины нет в списке", reply_markup=kb)
    else:
        await message.answer(text="Машина найдена", reply_markup=kb)
        text = (f"{user['fio']}, "
                f"тел. {user['phone']}")
        text += f", авто {user['car']} - {user['comment']}"
        await message.answer(text=text)

