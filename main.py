import ImgWrite
import ImgRead
import asyncio
import logging
import sys
from os import getenv
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, html, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

password = "piz koroche"

#ImgRead.ImgRead(password)



# Bot token can be obtained via https://t.me/BotFather
bot = Bot("7720479793:AAER4bnMoKTXXf5wd1e3PnJAHe6J3ZZAEso")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

isPassword = False
pasword = ""

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="записать пароль")]
        ],
        resize_keyboard=True  # Автоматически подгоняет размер кнопок
    )
    await message.answer(f"Hello, {message.from_user.full_name}!",reply_markup=keyboard)

DOWNLOAD_FOLDER = "downloaded_images"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@dp.message(lambda message: message.photo)
async def handle_photos(message: types.Message):
    # Получаем фото с максимальным качеством (последний элемент в массиве)
    photo = message.photo[-1]
    
    # Скачиваем файл
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    
    # Генерируем имя файла
    filename = os.path.join(DOWNLOAD_FOLDER, f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    
    # Сохраняем на диск
    await bot.download_file(file_path, destination=filename)
    ImgWrite.ImgWrite(password=password,message=message.caption,path=filename)
    #await message.answer(message.caption)

@dp.message(F.text == "записать пароль")
async def command_message_handler(message: Message):
    global isPassword
    isPassword = True
    await message.answer("Введите пароль")

@dp.message()
async def echo_handler(message: Message) -> None:
    global isPassword, pasword
    if isPassword == True:
        await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id)
        pasword = message.text
        print(pasword)
        await message.answer("Пароль успешно записан")
    isPassword = False

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
