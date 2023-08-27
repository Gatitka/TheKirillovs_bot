from aiogram import executor
from dispatcher import dp
import handlers

from db import BotDB
BotDB = BotDB('accountant.db')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)






# from aiogram import executor
# from dispatcher import dp
# import handlers

# from db import BotDB
# BotDB = BotDB('accountant.db')

# if __name__ == "__main__":


# # Здесь укажите токен,
# # который вы получили от @Botfather при создании бот-аккаунта
# bot = Bot(token='<6668401701:AAHzkj-BzehpQYl0spk8HgLz0O21tjnmSIk>')
# # Укажите id своего аккаунта в Telegram
# chat_id = <chat_id>
# text = 'Вам телеграмма!'
# # Отправка сообщения
# bot.send_message(chat_id, text)
