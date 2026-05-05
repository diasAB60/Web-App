import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

bot_token = "7780929287:AAESXU78-UZVwrTQsyJPJu3JlyVtxiUxRqc"
bot = Bot(token = bot_token)
dp = Dispatcher()

@dp.callback_query()
async def callback(callback: types.CallbackQuery):  
    await callback.answer()
    await callback.message.answer(callback.data)

@dp.message(Command('start'))
async def command_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text = 'Game store', web_app = WebAppInfo(url = 'https://itprogrer.com')))

    markup = builder.as_markup(resize_keyboard = True, one_time_keyboard = True)
    await message.answer('Hello! This bot helps you to buy a game. If you want to see game list please click the link below: ', reply_markup = markup)

    


async def main():
    await dp.start_polling(bot)

if (__name__ == "__main__"):
    asyncio.run(main())