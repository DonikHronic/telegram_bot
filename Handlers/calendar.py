from aiogram.dispatcher.filters import Command
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from loader import dp, bot


@dp.message_handler(Command('cal'))
async def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    await bot.send_message(m.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)



