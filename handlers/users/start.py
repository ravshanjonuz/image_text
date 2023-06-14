from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import Throttled

from handlers.users.admin import create_user
from loader import dp
from utils.db_api.sqlite import db


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
        await state.finish()

        try:
            create_user(message.chat.id, message.from_user.full_name)
        except:
            print(1)

        try:
            await message.answer(f"Assalomu Alaykum <b>{message.from_user.full_name}</b>. \n"
                             f"Menga shunchaki <b>🖼 rasm</b> yuboring men esa ichidagi matnlarni olib beraman",
                             parse_mode="HTML")
        except Exception as e:
            print(e)

