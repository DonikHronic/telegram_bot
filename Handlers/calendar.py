from aiogram.dispatcher.filters import Command
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from loader import dp, bot


@dp.message_handler(Command('cal'))
async def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    await bot.send_message(m.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@dp.callback_query_handler(DetailedTelegramCalendar.func())
async def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}", c.message.chat.id, c.message.message_id, reply_markup=key)
    elif result:
        await bot.edit_message_text(f"You selected {result}", c.message.chat.id, c.message.message_id)
