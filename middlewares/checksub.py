from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNELS, btn_accept
from loader import bot
from utils.misc import subscription


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id

        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        text_request_text = "🙂 Botdan to'liq va <b>BEPUL</b> foydalanish uchun telegram kanalimizga a'zo bo'ling"
        result = f"{text_request_text}:\n"
        final_status = True
        chs = []
        for channel in CHANNELS:
            status = await subscription.check(
                user_id=user,
                channel=channel
            )
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                chs.append([types.InlineKeyboardButton(channel.title, url=invite_link)])
        chs.append([types.InlineKeyboardButton(text=btn_accept, callback_data="check_subs")])
        if not final_status:
            await update.message.answer(result, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=chs),
                                        disable_web_page_preview=True)
            raise CancelHandler()
