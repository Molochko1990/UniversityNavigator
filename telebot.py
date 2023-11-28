import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from recognition import extract_route
from aiogram.types import FSInputFile
import navigator


TOKEN = '6418940022:AAGYidmVjFz8ovrFaDrfk8NrIFHeunra7k4'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command('start'))
async def cmd_reply(message: types.Message):
    await message.reply("Привет!\nЯ- Интеллектуальный Бот-Навигатор \nТы можешь найти маршрут от одной"
                        " точки до другой!\nВведи мне 2 точки в таком формате: Маршрут из Р-123 в Р-544 или Р-123 в Р-544")

@dp.message()
async def print_route(message: types.Message):
    start_room, end_room = extract_route(text=message.text).split(' ')
    image_files = navigator.build_path(start_room, end_room)
    if isinstance(image_files, str):
        await message.reply(image_files)
    else:
        for image_path in image_files:
            photo = FSInputFile(image_path)
            await bot.send_photo(message.chat.id, photo=photo)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
