import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from recognition import extract_route


TOKEN = '6418940022:AAGYidmVjFz8ovrFaDrfk8NrIFHeunra7k4'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command('start'))
async def cmd_reply(message: types.Message):
    await message.reply("Привет!\nЯ- Интеллектуальный Бот-Навигатор \nТы можешь найти маршрут от одной"
                        " точки до другой!\nВведи мне 2 точки: откуда надо построить маршрут и куда")


@dp.message()
async def print_route(message: types.Message):
    text = extract_route(text=message.text)
    print(text)
    await message.reply(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
