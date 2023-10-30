from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers.keyboards as kb
from dispatcher import BotDB

from .report import extract_value, prepare_report_message

CATEGORIES = ['food', 'auto', 'relax', 'Stepa',
              'education', 'flat', 'style', 'health']


class ExpencesStatesGroup(StatesGroup):
    category = State()
    expense = State()


# @dp.message_handler(commands='add_expence')
async def add_expence(message: types.Message):
    user_exists, no_tables = BotDB.user_exists(message.from_user.id)
    if no_tables:
        await message.answer("Бот еще не настроен.🛠",
                             reply_markup=kb.get_menu_kb())
    elif not user_exists:
        await message.answer("Вы не в списке участников.🤷‍♀️")
    else:
        await message.answer(
            "Выбери категорию и отправь сообщением затраты с комментарием,\n"
            + "например '500 кофе и сэндвичи'",
            reply_markup=kb.get_expenses_kb()
        )
        await ExpencesStatesGroup.category.set()
        # установили состояние категории
        await message.delete()


# @dp.callback_query_handler(text=CATEGORIES,
#                            state=ExpencesStatesGroup.category)
async def load_category(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=call.data)
    await ExpencesStatesGroup.expense.set()
    # установили состояние затрат


# @dp.message_handler(state=ExpencesStatesGroup.expense)
async def load_expense(message: types.Message, state: FSMContext):
    await state.update_data(expense=message.text)
    data = await state.get_data()
    category = data['category']
    value, comment = extract_value(message.text)
    if value:
        BotDB.add_record(message.from_user.id, category, value, comment)
        report_message = prepare_report_message()
        await message.reply(
            f'👌Запись о расходе успешно занесена!\n{report_message}',
            reply_markup=kb.get_menu_kb()
        )
        await state.finish()
    else:
        await message.reply(
            '🤓Ошибка в сумме затрат. Попробуйте внести заново.'
        )


def register_handlers_expences(dp: Dispatcher):
    dp.register_message_handler(add_expence, commands='add_expence')
    dp.register_callback_query_handler(load_category, text=CATEGORIES,
                                       state=ExpencesStatesGroup.category)
    dp.register_message_handler(load_expense,
                                state=ExpencesStatesGroup.expense)
