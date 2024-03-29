import sys

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from models.Car import Car
from router import form_router
from buttons import getMainButtons
from models.User import User
from stringUtils import transformCarNumber

import sqlite3


class CreateTenantForm(StatesGroup):
    chat_id = State()
    last_name = State()
    first_name = State()
    middle_name = State()
    phone = State()
    flat = State()
    car_number = State()
    add_more = State()


@form_router.message(F.text.lower() == "добавить жителя")
async def createTenant(message: Message, state: FSMContext):
    await state.set_state(CreateTenantForm.chat_id)
    await message.answer("Введите ЦИФРОВОЙ id жителя. Можно узнать, "
                         "переслав боту: @getmyid_bot любое сообщение от жителя", reply_markup=ReplyKeyboardRemove())


@form_router.message(CreateTenantForm.chat_id)
async def process_chat_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await state.set_state(CreateTenantForm.last_name)
    await message.answer("Введите фамилию")


@form_router.message(CreateTenantForm.last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(CreateTenantForm.first_name)
    await message.answer("Введите имя")


@form_router.message(CreateTenantForm.first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(CreateTenantForm.middle_name)
    await message.answer("Введите отчество")


@form_router.message(CreateTenantForm.middle_name)
async def process_middle_name(message: Message, state: FSMContext):
    await state.update_data(middle_name=message.text)
    await state.set_state(CreateTenantForm.phone)
    await message.answer("Введите номер телефона")


@form_router.message(CreateTenantForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(CreateTenantForm.flat)
    await message.answer("Введите номер квартиры")


@form_router.message(CreateTenantForm.flat)
async def process_flat(message: Message, state: FSMContext):
    await state.update_data(flat=message.text)
    await state.set_state(CreateTenantForm.car_number)
    await message.answer("Введите номер машины")


@form_router.message(CreateTenantForm.car_number)
async def process_car_number(message: Message, state: FSMContext):
    data = await state.get_data()
    car_numbers = data.get('car_numbers', None)
    if car_numbers is None:
        car_numbers = []
    car_numbers.append(transformCarNumber(message.text))
    await state.update_data(car_numbers=car_numbers)
    await state.set_state(CreateTenantForm.add_more)
    await message.answer("Ввести еще один автомобиль?",
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[
                                 KeyboardButton(text="Да"),
                                 KeyboardButton(text="Нет"),
                             ]
                             ],
                             resize_keyboard=True),
                         )


@form_router.message(CreateTenantForm.add_more, F.text.lower() == "да")
async def process_add_car(message: Message, state: FSMContext):
    await state.set_state(CreateTenantForm.car_number)
    await message.answer("Введите номер машины", reply_markup=ReplyKeyboardRemove())


@form_router.message(CreateTenantForm.add_more, F.text.lower() == "нет")
async def process_not_add(message: Message, state: FSMContext):
    data = await state.get_data()
    new_user_data = User()
    new_user_data.setupByDict(data)
    con = sqlite3.connect('parking_DB.sqlite3')
    cur = con.cursor()
    check = cur.execute('''SELECT * FROM users WHERE chat_id = ?''',
                        (new_user_data.chat_id,)).fetchall()
    if len(check) == 0:
        cur.execute('''INSERT INTO users(chat_id, permissions)''', (new_user_data.chat_id, 0))
    else:
        cur.execute('''UPDATE users SET permissions = ? WHERE chat_id = ?''',
                    (0, new_user_data.chat_id))
    cur.execute('''INSERT INTO usersdata(chat_id, fio, phone)''',
                (new_user_data.chat_id,
                 f"{new_user_data.last_name} {new_user_data.first_name} {new_user_data.middle_name}",
                 new_user_data.phone))
    for car in new_user_data.cars:
        cur.execute('''INSERT INTO cars(chat_id, car, comment)''',
                    (new_user_data.chat_id, car.number, 'Авто добавлено админисратором'))
    con.commit()
    con.close()
    await state.clear()
    buttons = getMainButtons(message.from_user.id)
    kb = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    await message.answer("Данные сохранены", reply_markup=kb)
    text = (f"{new_user_data.last_name} {new_user_data.first_name} {new_user_data.middle_name}, "
            f"тел. {new_user_data.phone}, кв. {new_user_data.flat}")
    for car in new_user_data.cars:
        text += f", авто {car.number}"
    await message.answer(text=text)
