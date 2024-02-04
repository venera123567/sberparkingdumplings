from aiogram import types
from store import roleStore

b1_admin = types.KeyboardButton(text='Добавить жителя')
b2_admin = types.KeyboardButton(text='Добавить админов')

b1_tenant = types.KeyboardButton(text='Скорректировать мои данные')
b2_tenant = types.KeyboardButton(text='Временные гости')

b1_security = types.KeyboardButton(text='Проверить номер машины')



b1_FIO = types.KeyboardButton(text='ФИО')
b2_num = types.KeyboardButton(text='Номер телефона')
b3_apart = types.KeyboardButton(text='Номер квартиры')


b1_plus_admins = types.KeyboardButton(text='Добавить администраторов')
b2_plus_tenant = types.KeyboardButton(text='Добавить жителя')

def getMainButtonsByRole(role):
    global b1_admin, b2_admin, b1_tenant, b2_tenant, b1_security
    if role == 'admin':
        return [b1_admin, b2_admin]
    elif role == 'security':
        return [b1_security]
    else:
        return [b1_tenant, b2_tenant]

def getMainButtons(user_id):
    global b1_admin, b2_admin, b1_tenant, b2_tenant, b1_security
    role = roleStore[user_id]
    return getMainButtonsByRole(role)