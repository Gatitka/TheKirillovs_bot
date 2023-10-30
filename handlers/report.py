import datetime
import re

from aiogram import Dispatcher, types

import handlers.keyboards as kb
from dispatcher import BotDB

REPORT = ['results_total_month', 'details_day', 'details_month']
MONTHLY_EXPENCES = 600
PERIOD_START = [2023, 10, 25]
PERIOD_END = [PERIOD_START[0], PERIOD_START[1]+1, PERIOD_START[2]-1]


def prepare_report_message():
    left = round(MONTHLY_EXPENCES - BotDB.get_records(), 2)
    days_left = (
        datetime.datetime(*PERIOD_END) - datetime.datetime.today()).days + 1
    daily_av = round(left / days_left, 2)
    return (f'Осталось:\n{left} € на {days_left} дней\n'
            + f'{daily_av} € - лимит трат на день')


def extract_value(expense: str):
    exp_split = expense.split()
    value = re.findall(r"\d+(?:.\d+)?", exp_split[0])
    if len(value):
        value = float(value[0].replace(',', '.'))
    else:
        value = None
    comment = ' '.join(exp_split[1:])
    return value, comment


# @dp.message_handler(commands=REPORT)
async def report_detailed(message: types.Message):
    user_exists, no_tables = BotDB.user_exists(message.from_user.id)
    if no_tables:
        await message.answer("Бот еще не настроен.🛠",
                             reply_markup=kb.get_menu_kb())
    elif not user_exists:
        await message.answer("Вы не в списке участников.🤷‍♀️")
    else:
        if message.text == '/results_total_month':
            result = BotDB.get_report_total_month(MONTHLY_EXPENCES)
        elif message.text == '/details_day':
            result = BotDB.get_report_details_day()
        elif message.text == '/details_month':
            result = BotDB.get_report_details_month()
        await message.answer(result, reply_markup=kb.get_menu_kb())
    await message.delete()


# @dp.message_handler(commands='report')
async def report(message: types.Message):
    user_exists, no_tables = BotDB.user_exists(message.from_user.id)
    if no_tables:
        await message.answer("Бот еще не настроен.🛠",
                             reply_markup=kb.get_menu_kb())
    elif not user_exists:
        await message.answer("Вы не в списке участников.🤷‍♀️")
    else:
        report_message = prepare_report_message()
        await message.answer(
            f'{report_message}',
            reply_markup=kb.get_report_kb()
        )


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(report_detailed, commands=REPORT)
    dp.register_message_handler(report, commands='report')
