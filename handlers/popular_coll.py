from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from parser_bot import popular_coll
from handlers.common import main_keyboard

day_coll = ('1', '7', '30')


class PopColl(StatesGroup):
    waiting_day_coll = State()


async def pop_coll_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in day_coll:
        keyboard.add(name)
    await message.answer("Введите промежуток времени (1, 7, 30) суток:", reply_markup=keyboard)
    await PopColl.waiting_day_coll.set()


async def pop_coll_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in day_coll:
        await message.answer("Такого промежутка не существует! Проверьте правильность введенных данных!")
        return
    await state.update_data(chosen_pop_coll=message.text.lower())
    await message.answer(popular_coll(message.text.lower()), reply_markup=main_keyboard())
    await state.finish()


def register_handlers_pop_coll(dp: Dispatcher):
    dp.register_message_handler(pop_coll_start, commands="pcoll", state='*')
    dp.register_message_handler(pop_coll_chosen, state=PopColl.waiting_day_coll)
