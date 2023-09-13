import handlers
import aiogram
from db import BotDB
from dispatcher import dp
import config

BotDB = BotDB(config.DB_FILE)
BotDB = BotDB()
# connection to DB on distant server

if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
