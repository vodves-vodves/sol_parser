from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from parser_bot import all_coll, floor_price_coll
from handlers.common import main_keyboard

name_coll = all_coll()


class FloorColl(StatesGroup):
    waiting_name_coll = State()


async def floor_coll_start(message: types.Message):
    await message.answer("Введите название коллекции:")
    await FloorColl.waiting_name_coll.set()


async def floor_coll_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in name_coll:
        await message.answer("Этой коллекции не существует! Проверьте правильность введенных данных!")
        return
    await state.update_data(chosen_floor_coll=message.text.lower())
    await message.answer(floor_price_coll(message.text.lower()), reply_markup=main_keyboard())
    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено', reply_markup=main_keyboard())


def register_handlers_floor_coll(dp: Dispatcher):
    dp.register_message_handler(floor_coll_start, commands="fcoll", state='*')
    dp.register_message_handler(floor_coll_chosen, state=FloorColl.waiting_name_coll)
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state='*')
