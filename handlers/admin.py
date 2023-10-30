from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers.keyboards as kb
from dispatcher import BotDB

SETTINGS = ['create_tables',
            'add_user', 'delete_user',
            'add_admin', 'delete_admin']


class AdminStatesGroup(StatesGroup):
    add_user = State()
    del_user = State()
    add_admin = State()
    del_admin = State()
    choice = State()


# @dp.message_handler(commands='admin-panel')
async def start_settings(message: types.Message):
    if BotDB.is_admin(message.from_user.id):
        await message.answer(
            "Выбери команду для следующего действия:",
            reply_markup=kb.get_admin_panel_kb()
        )
        await AdminStatesGroup.choice.set()
    await message.delete()


# @dp.callback_query_handler(text=SETTINGS, state=AdminStatesGroup.choice)
async def settings(call: types.CallbackQuery):
    await call.answer('Внесите ID пользователя.')
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


# @dp.message_handler(state=AdminStatesGroup.add_user)
async def add_user(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_user('add', user_id)
    await message.reply('🤠Пользователь успешно добавлен.',
                        reply_markup=kb.get_admin_panel_kb())
    await state.finish()


# @dp.message_handler(state=AdminStatesGroup.del_user)
async def del_user(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_user('del', user_id)
    await message.reply('😵Пользователь успешно удален.',
                        reply_markup=kb.get_admin_panel_kb())
    await state.finish()


# @dp.message_handler(state=AdminStatesGroup.add_admin)
async def add_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_admin('add', user_id)
    await message.reply('🤩Админ успешно добавлен.',
                        reply_markup=kb.get_admin_panel_kb())
    await state.finish()


# @dp.message_handler(state=AdminStatesGroup.del_admin)
async def del_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    BotDB.manage_admin('del', user_id)
    await message.reply('🥶Админ успешно удален.',
                        reply_markup=kb.get_admin_panel_kb())
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_settings, commands=['admin-panel'])
    dp.register_callback_query_handler(settings, text=SETTINGS,
                                       state=AdminStatesGroup.choice)
    dp.register_message_handler(add_user, state=AdminStatesGroup.add_user)
    dp.register_message_handler(del_user, state=AdminStatesGroup.del_user)
    dp.register_message_handler(add_admin, state=AdminStatesGroup.add_admin)
    dp.register_message_handler(del_admin, state=AdminStatesGroup.del_admin)
