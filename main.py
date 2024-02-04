import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message
import sqlite3
from config import TOKEN_API
from stringUtils import transformCarNumber
from changeDataForm import ChangeDataForm
from createTenantForm import CreateTenantForm
from searchCarNumberForm import SearchCarNumberForm
from router import form_router
from store import roleStore
from buttons import getMainButtonsByRole

bot = Bot(TOKEN_API)
dp = Dispatcher()


con = sqlite3.connect('parking_DB.sqlite3')
cur = con.cursor()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = cur.execute('''SELECT * FROM users WHERE chat_id=?''', (message.from_user.id,)).fetchall()
    try:
        if user[0][2] == 2:
            roleStore[message.from_user.id] = 'admin'
            kb_admin_buttons = getMainButtonsByRole('admin')
            kb_admin = ReplyKeyboardMarkup(keyboard=[kb_admin_buttons], resize_keyboard=True)
            await bot.send_sticker(chat_id=message.from_user.id, sticker="CAACAgIAAxkBAAELUAABZb86g3bdM6o8ROdJ139VrtvBtYMAAvw-AAL-dQFKbSV49k-mUF40BA", reply_markup=kb_admin)
        elif user[0][2] == 1:
            roleStore[message.from_user.id] = 'security'
            kb_security_buttons = getMainButtonsByRole('security')
            kb_security = ReplyKeyboardMarkup(keyboard=[kb_security_buttons], resize_keyboard=True)
            await bot.send_sticker(chat_id=message.from_user.id, sticker="CAACAgIAAxkBAAELUAZlvzqVn2Ft7ShSIIYE50CBhlhvUAACpUAAAiolAAFK4fWw_8FAxzo0BA", reply_markup=kb_security)
        elif user[0][2] == 0:
            roleStore[message.from_user.id] = 'tenant'
            kb_tenant_buttons = getMainButtonsByRole('tenant')
            kb_tenant = ReplyKeyboardMarkup(keyboard=[kb_tenant_buttons], resize_keyboard=True)
            await bot.send_sticker(chat_id=message.from_user.id, sticker="CAACAgIAAxkBAAELUAFlvzqEN8ccBd-LGiEdNw-lN2_NVQACgkkAAvxd-UmsGcBeJcWzGDQE", reply_markup=kb_tenant)
    except IndexError:
        await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAELUF1lv2UU9IQrDu5Gj5cg_ZcvG1I5tQAC1TwAAqm8-Ul3BnglWYK4BjQE')
        print(message.from_user.id)


@dp.message(F.text.lower() == "добавить администратора")
async def with_puree(message: types.Message):
    await message.answer("")


# @dp.message(F.text.lower() == "добавить жителя")
# async def with_puree(message: types.Message):
#     await message.answer("Введите данные жителя")


@dp.message(F.text.lower() == "временные гости")
async def with_puree(message: types.Message):
    await message.answer("Введите номер машины гостя и его время прибывания на стоянке")


# @dp.message(F.text.lower() == "скорректировать мои данные")
# async def with_puree(message: types.Message):
#     global b1_FIO, b2_num, b3_apart
#     kb_change = ReplyKeyboardMarkup(keyboard=[[b1_FIO, b2_num, b3_apart]], resize_keyboard=True)
#     await message.answer("Что вы хотите изменить?", reply_markup=kb_change)

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
    dp.include_router(form_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())