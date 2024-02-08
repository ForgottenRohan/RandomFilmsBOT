from aiogram import Bot, types, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.enums import parse_mode
import asyncio
import sqlite3
import random

bot = Bot(token='BOT', parse_mode=parse_mode.ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply("<b>Hello!</b>\nI'm a bot that can help you find a film!\n\nTo start, send me a command: /film")


@dp.message(Command('film'))
async def film(message: types.Message):
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('''SELECT name, info, link FROM films''')
        film = random.choice(cursor.fetchall())
        await message.reply(f"<b>{film[0]}</b>\n\n{film[1]}\n\n<a>{film[2]}</a>")
        print('Film send')
        connect.close()
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())