import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from db import BotDB

# from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter


# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

# init
storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
BotDB = BotDB(config.DB_FILE)
# connection to DB on distant server
dp = Dispatcher(bot, storage=storage)

# # activate filters
# dp.filters_factory.bind(IsOwnerFilter)
# dp.filters_factory.bind(IsAdminFilter)
# dp.filters_factory.bind(MemberCanRestrictFilter)
