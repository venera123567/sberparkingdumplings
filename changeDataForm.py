from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from router import form_router
from buttons import getMainButtons
from models.User import User

import sqlite3


class ChangeDataForm(StatesGroup):
    last_name = State()
    first_name = State()
    middle_name = State()
    phone = State()
    flat = State()

@form_router.message(F.text.lower() == "скорректировать мои данные")
async def req_fio_liver(message: Message, state: FSMContext):
    await state.set_state(ChangeDataForm.last_name)
    await message.answer("Введите новую фамилию", reply_markup=ReplyKeyboardRemove())

@form_router.message(ChangeDataForm.last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(ChangeDataForm.first_name)
    await message.answer("Введите новое имя")

@form_router.message(ChangeDataForm.first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(ChangeDataForm.middle_name)
    await message.answer("Введите новое отчество")

@form_router.message(ChangeDataForm.middle_name)
async def process_middle_name(message: Message, state: FSMContext):
    await state.update_data(middle_name=message.text)
    await state.set_state(ChangeDataForm.phone)
    await message.answer("Введите новый номер телефона")

@form_router.message(ChangeDataForm.phone)
async def process_phone(message: Message, state: FSMContext):
        await state.update_data(phone=message.text)
        await state.set_state(ChangeDataForm.flat)
        await message.answer("Введите новый номер квартиры")

@form_router.message(ChangeDataForm.flat)
async def process_flat(message: Message, state: FSMContext):
        await state.update_data(flat=message.text)
        data = await state.get_data()
        new_user_data = User()
        new_user_data.setupByDict(data)
        # сохранение в БД
        con = sqlite3.connect('parking_DB.sqlite3')
        cur = con.cursor()
        user_from_bd = cur.execute('''SELECT id FROM usersdata WHERE chat_id = ?''', (message.from_user.id,)).fetchall()
        if len(user_from_bd) == 0:
            cur.execute('''INSERT INTO usersdata(chat_id, fio, phone) VALUES(?, ?, ?)''',
                        (message.from_user.id, 'ФИО отсутствует', 'Телефон отсутствует'))
        cur.execute('''UPDATE usersdata SET fio = ?
                                WHERE chat_id = ?''',
                    (f'{new_user_data.last_name} {new_user_data.first_name} {new_user_data.middle_name}',
                     message.from_user.id))
        cur.execute('''UPDATE usersdata SET phone = ?
                                WHERE chat_id = ?''',
                    (str(new_user_data.phone), message.from_user.id))
        user_from_bd = cur.execute('''SELECT user_id FROM tenants WHERE user_id = ?''',
                                   (message.from_user.id,)).fetchall()
        if len(user_from_bd) == 0:
            cur.execute('''INSERT INTO tenants(user_id, appartment) VALUES(?, ?)''',
                        (message.from_user.id, 'Квартира отсутсвует'))
        cur.execute('''UPDATE tenants SET appartment = ?
                                WHERE user_id = ?''',
                    (str(new_user_data.flat), message.from_user.id))
        con.commit()
        con.close()
        await state.clear()
        buttons = getMainButtons(message.from_user.id)
        kb = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
        await message.answer("Данные сохранены", reply_markup=kb)
        text = (f"Новые данные: {new_user_data.last_name} {new_user_data.first_name} {new_user_data.middle_name}, "
                f"тел. {new_user_data.phone}, кв. {new_user_data.flat}")
        await message.answer(text=text, reply_markup=kb)
