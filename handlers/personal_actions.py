from aiogram import types
from aiogram.types import (ReplyKeyboardMarkup,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from dispatcher import dp
import re
from bot import BotDB
import math


MONTHLY_EXPENCES = 300


# START keyboard
keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
keyboard_start.add('/menu')

# START ADMIN-PANEL keyboard
keyboard_admin_start = ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
keyboard_admin_start.add('/menu').add('/admin-panel')

# START keyboard
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
keyboard_menu.add('/add_expence').add('/report').add('/start')

# EXPENSES CATEGORY keyboard
keyboard_exp = InlineKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)

button3 = InlineKeyboardButton(text='🍽food', callback_data='food')
button4 = InlineKeyboardButton(text='🚙auto', callback_data='auto')
button5 = InlineKeyboardButton(text='🏕relax', callback_data='travel')
button6 = InlineKeyboardButton(text='🤹‍♂️Stepa', callback_data='Stepa')
button7 = InlineKeyboardButton(text='🎓education', callback_data='know-how')
button8 = InlineKeyboardButton(text='🏠flat', callback_data='flat')
button9 = InlineKeyboardButton(text='👘style', callback_data='style')
button16 = InlineKeyboardButton(text='👩🏻‍🔬health', callback_data='health')
button10 = InlineKeyboardButton(text='🔙menu', callback_data='menu')

keyboard_exp.row(button3, button4, button5, button6)
keyboard_exp.row(button7, button8, button9, button16)
# keyboard_exp.add(button10)    # backwards not working properly

# ADMIN-PANEL keyboard
keyboard_admin = InlineKeyboardMarkup(resize_keyboard=True,
                                      one_time_keyboard=True)

button11 = InlineKeyboardButton(text='create_tables',
                                callback_data='create_tables')
button12 = InlineKeyboardButton(text='add_user', callback_data='add_user')
button13 = InlineKeyboardButton(text='delete_user',
                                callback_data='delete_user')
button14 = InlineKeyboardButton(text='add_admin', callback_data='add_admin')
button15 = InlineKeyboardButton(text='del_admin', callback_data='delete_admin')

keyboard_admin.row(button12, button13)
keyboard_admin.row(button14, button15)
keyboard_admin.add(button11)
# keyboard_admin.add(button10)    # backwards not working properly

CATEGORIES = ['food', 'auto', 'relax', 'Stepa',
              'education', 'flat', 'style', 'health']
SETTINGS = ['create_tables',
            'add_user', 'delete_user',
            'add_admin', 'delete_admin']


class ExpencesStatesGroup(StatesGroup):
    category = State()
    expense = State()


class AdminStatesGroup(StatesGroup):
    add_user = State()
    del_user = State()
    add_admin = State()
    del_admin = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать!\nНажми /menu для входа в учет затрат.",
        reply_markup=keyboard_start
    )
    if BotDB.isAdmin(message.from_user.id):
        await message.answer(
            "Вы авторизовались как администратор и вам доступна команда\n"
            + "/admin_panel для создания базы данных, "
            + "управления пользователями и админами",
            reply_markup=keyboard_admin_start
        )
    await message.delete()


@dp.message_handler(commands='menu')
async def menu(message: types.Message):
    await message.answer(
        "Выбери команду для следующего действия:\n"
        + "💸/add_expence - добавить затраты\n"
        + "📉/report - увидеть отчет"
        + "/start - вернуться в основное меню",
        reply_markup=keyboard_menu
    )
    await message.delete()


@dp.message_handler(commands='admin-panel')
async def start_settings(message: types.Message):
    if BotDB.isAdmin(message.from_user.id):
        await message.answer(
            "Выбери команду для следующего действия:",
            reply_markup=keyboard_admin
        )
    await message.delete()


@dp.message_handler(commands='add_expence')
async def add_expence(message: types.Message):
    user_exists, no_tables = BotDB.user_exists(message.from_user.id)
    if no_tables:
        await message.answer("Бот еще не настроен.🛠", reply_markup=keyboard_menu)
    elif not user_exists:
        await message.answer("Вы не в списке участников.🤷‍♀️")
    else:
        await message.answer(
            "Выбери категорию и отправь сообщением затраты с комментарием,\n"
            + "например '500 кофе и сэндвичи'",
            reply_markup=keyboard_exp
        )
        await ExpencesStatesGroup.category.set()
        # установили состояние категории
        await message.delete()


@dp.callback_query_handler(text=CATEGORIES, state=ExpencesStatesGroup.category)
async def load_category(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=call.data)
    await ExpencesStatesGroup.expense.set()
    # установили состояние затрат


@dp.message_handler(state=ExpencesStatesGroup.expense)
async def load_expense(message: types.Message, state: FSMContext):
    await state.update_data(expense=message.text)
    data = await state.get_data()
    category = data['category']
    value, comment = extract_value(message.text)
    if value:
        BotDB.add_record(message.from_user.id, category, value, comment)
        left = round(MONTHLY_EXPENCES - BotDB.get_records(), 2)
        await message.reply(
            f'👌Запись о расходе успешно занесена! Осталось {left}.',
            reply_markup=keyboard_menu
        )
        await state.finish()
    else:
        await message.reply(
            '🤓Ошибка в сумме затрат. Попробуйте внести заново.'
        )


def extract_value(expense: str):
    exp_split = expense.split()
    value = re.findall(r"\d+(?:.\d+)?", exp_split[0])
    if len(value):
        value = float(value[0].replace(',', '.'))
    else:
        value = None
    comment = ' '.join(exp_split[1:])
    return value, comment


@dp.callback_query_handler(text=SETTINGS)
async def settings(call: types.CallbackQuery):
    if call.data == 'create_tables':
        BotDB.create_db_tables()
        await call.answer(
            '👌Таблицы баз данных успешно созданы.'
        )
    elif call.data == 'add_user':
        await AdminStatesGroup.add_user.set()
    elif call.data == 'delete_user':
        await AdminStatesGroup.del_user.set()
    elif call.data == 'add_admin':
        await AdminStatesGroup.add_admin.set()
    elif call.data == 'delete_admin':
        await AdminStatesGroup.del_admin.set()


@dp.message_handler(state=AdminStatesGroup.add_user)
async def add_user(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_user('add', user_id)
    await message.reply('🤠Пользователь успешно добавлен.',
                        reply_markup=keyboard_admin)
    await state.finish()


@dp.message_handler(state=AdminStatesGroup.del_user)
async def del_user(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_user('del', user_id)
    await message.reply('😵Пользователь успешно удален.',
                        reply_markup=keyboard_admin)
    await state.finish()


@dp.message_handler(state=AdminStatesGroup.add_admin)
async def add_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_admin('add', user_id)
    await message.reply('🤩Админ успешно добавлен.',
                        reply_markup=keyboard_admin)
    await state.finish()


@dp.message_handler(state=AdminStatesGroup.del_admin)
async def del_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_admin('del', user_id)
    await message.reply('🥶Админ успешно удален.',
                        reply_markup=keyboard_admin)
    await state.finish()


@dp.message_handler(commands='report')
async def report(message: types.Message):
    user_exists, no_tables = BotDB.user_exists(message.from_user.id)
    if no_tables:
        await message.answer("Бот еще не настроен.🛠", reply_markup=keyboard_menu)
    elif not user_exists:
        await message.answer("Вы не в списке участников.🤷‍♀️")
    else:
        left = round(MONTHLY_EXPENCES - BotDB.get_records(), 2)
        await message.answer(f'Осталось {left}!', reply_markup=keyboard_menu)


@dp.message_handler()
async def reply(message: types.Message):
    await message.reply("Я тебя не понимаю.")
