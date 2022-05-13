from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter


def main_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Поиск коллекции', callback_data='coll_f'),
        types.InlineKeyboardButton(text='Популярные коллекции', callback_data='coll_p')
    ]
    main_keyboard = types.InlineKeyboardMarkup(row_width=2)
    main_keyboard.add(*buttons)
    return main_keyboard


async def commands(call: types.CallbackQuery):
    action = call.data.split('_')[1]
    if action == 'p':
        await call.message.answer('/pcoll')
    elif action == 'f':
        await call.message.answer('/fcoll')
    await call.answer()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите, что хотите парсить:', reply_markup=main_keyboard())


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено', reply_markup=main_keyboard())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_callback_query_handler(commands, Text(startswith="coll_"))
