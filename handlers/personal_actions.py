from aiogram import types
from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from dispatcher import dp
import re
from bot import BotDB

MONTHLY_EXPENCES = 600

button1 = KeyboardButton('/add_expence')
button2 = KeyboardButton('/report')
keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
keyboard_start.add(button1).add(button2)

button3 = InlineKeyboardButton(text='🍽food', callback_data='food')
button4 = InlineKeyboardButton(text='🚙auto', callback_data='auto')
button5 = InlineKeyboardButton(text='🏕travel', callback_data='travel')
button6 = InlineKeyboardButton(text='🤹‍♂️Stepa', callback_data='Stepa')
button7 = InlineKeyboardButton(text='🎓know-how', callback_data='know-how')
button8 = InlineKeyboardButton(text='🏠flat', callback_data='flat')
button9 = InlineKeyboardButton(text='👘style', callback_data='style')
button10 = InlineKeyboardButton(text='🔙/menu', callback_data='/menu')

keyboard_exp = InlineKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
keyboard_exp.row(button3, button4, button5, button6)
keyboard_exp.row(button7, button8, button9)
keyboard_exp.add(button10)

CATEGORIES = ['food', 'auto', 'travel', 'Stepa', 'know-how', 'flat', 'style']


class ExpencesStatesGroup(StatesGroup):
    category = State()
    expense = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        await message.bot.send_message(message.from_user.id, "Вас не звали!")

    await message.bot.send_message(
        message.from_user.id,
        "Добро пожаловать, выбери команду для следующего действия:\n"
        + "/add_expence - добавить затраты\n"
        + "/report - увидеть отчет",
        reply_markup=keyboard_start
    )


@dp.message_handler(commands='menu')
async def menu(message: types.Message):
    await message.bot.send_message(
        message.from_user.id,
        "Добро пожаловать, выбери команду для следующего действия:\n"
        + "/add_expence - добавить затраты\n"
        + "/report - увидеть отчет",
        reply_markup=keyboard_start
    )


@dp.message_handler(commands='add_expence')
async def add_expence(message: types.Message):
    await message.bot.send_message(
        message.from_user.id,
        "Выбери категорию:",
        reply_markup=keyboard_exp
    )
    await ExpencesStatesGroup.category.set()     # установили сост категории


@dp.callback_query_handler(text=CATEGORIES, state=ExpencesStatesGroup.category)
async def load_category(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'menu':
        await state.finish()

    await state.update_data(category=call.data)
    await ExpencesStatesGroup.expense.set()    # установили сост затрат


@dp.message_handler(state=ExpencesStatesGroup.expense)
async def load_expense(message: types.Message, state: FSMContext):
    await state.update_data(expense=message.text)
    data = await state.get_data()
    category = data['category']
    value, comment = extract_value(message.text)
    if value:
        BotDB.add_record(message.from_user.id, category, value, comment)
        left = MONTHLY_EXPENCES - BotDB.get_records()[0]
        await message.bot.send_message(
            message.from_user.id,
            f'Запись о расходе успешно занесена! Осталось {left}.'
        )
        await state.finish()
    else:
        await message.bot.send_message(
            message.from_user.id,
            'Ошибка в сумме затрат. Попробуйте внести заново.'
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


@dp.message_handler(commands='report')
async def report(message: types.Message):
    left = MONTHLY_EXPENCES - BotDB.get_records()[0]
    await message.reply(f'Осталось {left}!')
