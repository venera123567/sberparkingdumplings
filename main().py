import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import sqlite3
from config import TOKEN_API
from stringUtils import transformCarNumber


bot = Bot(TOKEN_API)
dp = Dispatcher()


con = sqlite3.connect('parking_DB.sqlite3')
cur = con.cursor()

b1_admin = types.KeyboardButton(text='Добавить жителя')
b2_admin = types.KeyboardButton(text='Добавить админов')

b1_tenant = types.KeyboardButton(text='Скорректировать мои данные')
b2_tenant = types.KeyboardButton(text='Временные гости')

b1_security = types.KeyboardButton(text='Просматривать записи')



b1_FIO = types.KeyboardButton(text='ФИО')
b2_num = types.KeyboardButton(text='Номер телефона')
b3_apart = types.KeyboardButton(text='Номер квартиры')


b1_plus_admins = types.KeyboardButton(text='Добавить администраторов')
b2_plus_tenant = types.KeyboardButton(text='Добавить жителя')


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = cur.execute('''SELECT * FROM users WHERE chat_id=?''', (message.from_user.id,)).fetchall()
    global b1_admin, b2_admin, b1_tenant, b2_tenant, b1_security
    kb_admin = ReplyKeyboardMarkup(keyboard=[[b1_admin, b2_admin]], resize_keyboard=True)
    kb_tenant = ReplyKeyboardMarkup(keyboard=[[b1_tenant, b2_tenant]], resize_keyboard=True)
    kb_security = ReplyKeyboardMarkup(keyboard=[[b1_security]], resize_keyboard=True)

    try:
        if user[0][3] == 2:
            await bot.send_message(chat_id=message.from_user.id, text=f'Hello admin!', reply_markup=kb_admin)
        elif user[0][3] == 1:
            await bot.send_message(chat_id=message.from_user.id, text=f'Hello security!', reply_markup=kb_security)
        elif user[0][3] == 0:
            await bot.send_message(chat_id=message.from_user.id, text=f'Hello tenant!', reply_markup=kb_tenant)
    except IndexError:
        await bot.send_message(chat_id=message.from_user.id, text=f'NOT FOUND: {message.from_user.id}')
        print(message.from_user.id)


@dp.message(F.text.lower() == "добавить администратора")
async def with_puree(message: types.Message):
    await message.answer("")


@dp.message(F.text.lower() == "добавить жителя")
async def with_puree(message: types.Message):
    await message.answer("Введите данные жителя")


@dp.message(F.text.lower() == "временные гости")
async def with_puree(message: types.Message):
    await message.answer("Введите номер машины гостя и его время прибывания на стоянке")


@dp.message(F.text.lower() == "скорректировать мои данные")
async def with_puree(message: types.Message):
    global b1_FIO, b2_num, b3_apart
    kb_change = ReplyKeyboardMarkup(keyboard=[[b1_FIO, b2_num, b3_apart]], resize_keyboard=True)
    await message.answer("Что вы хотите изменить?", reply_markup=kb_change)


@dp.message(F.text.lower() == "фио")
async def fio_liver(message: types.Message):
    await message.answer("Введите новое ФИО")


@dp.message(F.text.lower() == "номер телефона")
async def num_liver(message: types.Message):
    await message.answer("Введите новый номер телефона")


@dp.message(F.text.lower() == "номер квартиры")
async def apart_liver(message: types.Message):
    await message.answer("Введите новый номер квартиры")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())