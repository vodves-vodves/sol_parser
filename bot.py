import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.floor_price_coll import register_handlers_floor_coll
from handlers.popular_coll import register_handlers_pop_coll
from handlers.common import register_handlers_common


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/fcoll', description='Floor цена коллекции'),
        BotCommand(command='/pcoll', description='Популярные коллекции'),
        BotCommand(command='/cancel', description='Отмена')
    ]
    await bot.set_my_commands(commands)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error('Starting bot')


    bot = Bot(token='')
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_floor_coll(dp)
    register_handlers_pop_coll(dp)
    register_handlers_common(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())