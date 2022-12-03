from aiogram.utils import executor
from bot.create_bot import dp
import handlers
import datetime

handlers.register_handler(dp)
print("Бот запущен " + str(datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")))
executor.start_polling(dp, skip_updates=True)
