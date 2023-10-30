import aiogram

import config
from db import BotDB
from dispatcher import dp
from handlers import admin, expences, other, report

BotDB = BotDB(config.DB_FILE)
# connection to DB on distant server

if __name__ == "__main__":
    MONTHLY_EXPENCES = 600
    PERIOD_START = [2023, 10, 25]
    PERIOD_END = [PERIOD_START[0], PERIOD_START[1]+1, PERIOD_START[2]-1]

    admin.register_handlers_admin(dp)
    report.register_handlers_report(dp)
    expences.register_handlers_expences(dp)
    other.register_handlers_other(dp)
    aiogram.executor.start_polling(dp, skip_updates=True)
