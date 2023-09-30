import aiogram

import config
import handlers
from db import BotDB
from dispatcher import dp

BotDB = BotDB(config.DB_FILE)
# connection to DB on distant server

if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
