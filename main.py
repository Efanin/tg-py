import asyncio
import logging
import sys
from os import getenv
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, html, F, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiosqlite
import mode
# Bot token can be obtained via https://t.me/BotFather
bot = Bot("token")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()






@dp.message(CommandStart()) 
async def command_start_handler(message: Message) -> None:
    await start_user(message)
    await start_admin(message)



@mode.user
async def start_user(message: Message):
    await message.answer(f"Hello user, {html.bold(message.from_user.full_name)}!")


@mode.admin
async def start_admin(message: Message):
    await message.answer(f"Hello admin, {html.bold(message.from_user.full_name)}!")
    


@dp.message(Command("admin"))
async def echo_handler(message: Message) -> None:
    if True:
        mode.state = "admin"
        await message.answer("вы админ")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
