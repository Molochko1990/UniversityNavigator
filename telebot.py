import asyncio
import aiohttp
from aiogram import *
from aiogram.types import FSInputFile
import navigator
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Choice
from vizual_photo import visual
global start_room_g
from recognition import extract_route, fixer


TOKEN = '6418940022:AAGYidmVjFz8ovrFaDrfk8NrIFHeunra7k4'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command('start'))
async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Поиск по фото"),
            types.KeyboardButton(text="Поиск по строчке")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ поиска маршрута"
    )
    await message.answer("Привет!\nЯ- Интеллектуальный Бот-Навигатор \nТы можешь найти маршрут от одной"
                         " точки до другой!\nВыбери действие", reply_markup=keyboard)


@dp.message(F.text.lower() == "поиск по фото")
async def photo(message: types.Message, state: FSMContext):
    await message.reply("Отправьте фото")
    await state.set_state(Choice.photo)


@dp.message(F.text.lower() == "поиск по строчке")
async def string(message: types.Message, state: FSMContext):
    await message.answer("Откуда и куда?")
    await state.set_state(Choice.string)


@dp.message(Choice.string)
async def get_string(message: types.Message, state: FSMContext):
    Result = extract_route(message.text)
    start_room, end_room = Result
    image_files = navigator.build_path(start_room, end_room)
    if end_room == start_room: await message.answer("У самурая нет путь")
    for image_path in image_files:
        photo = FSInputFile(image_path)
        await bot.send_photo(message.chat.id, photo=photo)
    await state.clear()


@dp.message(Choice.photo)
async def get_photo(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file.file_path}'
        await bot.download_file(file.file_path, "D:\\photo.png", chunk_size=1024)
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status == 200:
                    global start_room_g
                    start_room_g = visual()
                    if start_room_g == "Не могу распознать фото":
                        await message.answer(start_room_g)
                    else:
                        await message.answer('Введите конечную координату')
                else:
                    print(f"Ошибка при загрузке файла: {resp.status}")
    else:
        end_room = fixer(message.text)
        start_room_g = fixer(start_room_g)
        #print(start_room_g, end_room)
        image_files = navigator.build_path(start_room_g, end_room)
        for image_path in image_files:
            photo = FSInputFile(image_path)
            await bot.send_photo(message.chat.id, photo=photo)
        await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
