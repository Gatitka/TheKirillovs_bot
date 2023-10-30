import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import BotDB
import config


# from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter


# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

storage = MemoryStorage()

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
BotDB = BotDB(config.DB_FILE)








# # activate filters
# dp.filters_factory.bind(IsOwnerFilter)
# dp.filters_factory.bind(IsAdminFilter)
# dp.filters_factory.bind(MemberCanRestrictFilter)
