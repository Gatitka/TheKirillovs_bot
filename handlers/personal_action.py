from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotDB

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!")

@dp.message_handler(commands = ("spent", "s"), commands_prefix = "/!")
async def record(message: types.Message):
    cmd_variants = ('/spent', '/s', '!spent', '!s')
    operation = '-'
    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if len(value):
        x = re.findall(r"\d+(?:.\d+)?", value)

        if len(x):
            value = float(x[0].replace(',', '.'))
            BotDB.add_record(message.from_user.id, operation, value)
            if operation == '-':
                await message.reply('Запись о расходе успешно занесена!')
        else:
            await message.reply('Не удалось определить сумму!')
    else:
        await message.reply('Не введена сумма!')

@dp.message_handler(commands = "report")
async def start(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!")
