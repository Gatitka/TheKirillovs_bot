import handlers
import aiogram
from db import BotDB
from dispatcher import dp

BotDB = BotDB('accountant.db')
# BotDB = BotDB('/home/Admin/TheKirillovs_bot/accountant.db')
# connection to DB on distant server

if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
