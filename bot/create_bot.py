from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
