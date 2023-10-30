from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import handlers.keyboards as kb
from dispatcher import BotDB


# @dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать!\nНажми /menu для входа в учет затрат.",
        reply_markup=kb.get_start_kb()
    )
    if BotDB.is_admin(message.from_user.id):
        await message.answer(
            "Вы авторизовались как администратор и вам доступна команда\n"
            + "/admin_panel для создания базы данных, "
            + "управления пользователями и админами",
            reply_markup=kb.get_start_admin_kb()
        )
    await message.delete()


# @dp.message_handler(commands='menu')
async def menu(message: types.Message):
    await message.answer(
        "Выбери команду для следующего действия:\n"
        + "💸/add_expence - добавить затраты\n"
        + "📉/report - увидеть отчет"
        + "/start - вернуться в основное меню",
        reply_markup=kb.get_menu_kb()
    )
    await message.delete()


# @dp.callback_query_handler(text='cancel', state='*')
async def cancel(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await call.message.delete()
        return
    await state.finish()
    await call.answer("Запись отменена.")
    await call.message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.callback_query_handler(cancel, text='cancel', state='*')
