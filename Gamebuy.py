import asyncio
import os
import sqlite3
import time
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'webStore_feedbacks.db')

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS feedback \
(id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
username TEXT,
feedback_type TEXT,
time INTEGER)''')
conn.commit()
cur.close()
conn.close()



bot_token = "7780929287:AAEEi2ceOsRVIvSscs4bkiS9VS5lUrsylFM"
bot = Bot(token = bot_token)
dp = Dispatcher()


@dp.message(Command('start'))
async def command_start(message: types.Message):
    
    
    await message.answer(f"Hello {message.from_user.first_name}! This bot helps you to buy a game. If you want to buy a game or see game list please click <b>'Game store' </b> button🤝: ", parse_mode = 'html')

    buttons = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text = " Game store ",web_app = WebAppInfo(url = 'https://diasab60.github.io/Web-App/'))
    btn2 = types.KeyboardButton(text = " This bot helped me 👍!")
    btn3 = types.KeyboardButton(text = " This bot didn't help me👎🏻! It needs update ")
    buttons.row(btn1)
    buttons.row(btn2, btn3) 
    await message.answer("And if not hard, please leave feedback 🙏🏻", reply_markup = buttons.as_markup(resize_keyboard = True))


@dp.message(F.text)
async def buttons_handler(message):
    if (message.chat.type == 'private'):

        if (message.text == "This bot helped me 👍!"):
            await message.answer("We're glad to hear it! Our bot is getting better and better every day! 🙏🏻")
    
        elif (message.text == "This bot didn't help me👎🏻! It needs update"):
            markup = InlineKeyboardBuilder()
            markup.button(text = "Bot is slow", callback_data = 'error_slow')
            markup.button(text = "Store is not working correctly", callback_data = 'error_store')
            markup.button(text = "Not many functions", callback_data = 'error_functions')
            markup.button(text = "Others", callback_data = 'error_others')

            markup.adjust(2)

            await message.answer("Our apologies. What exactly did you dislike about our bot? 🙌", reply_markup = markup.as_markup())


@dp.callback_query()
async def bot_buttons_handler(call: types.CallbackQuery):
    if (call.data.startswith("error")):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute('''INSERT INTO feedback(user_id, username, feedback_type, time) VALUES(?, ?, ?, ?)''', 
                    (call.from_user.id, 
                    call.from_user.username, 
                    call.data, 
                    int(time.time()
                    )
                )
            )

        conn.commit()
        conn.close()

    if (call.data == 'error_slow'):
        await call.answer("Thank you for feedback. We are already working on our bot's slowness! 🫰🏻")

    elif (call.data == 'error_store'):
        await call.answer('Thank you for feedback. We are already working on our store! 🫰🏻')    

    elif (call.data == 'error_functions'):
        await call.answer("Thank you for feedback. We are already improving out bot's functionality! 🫰🏻") 

    elif (call.data == 'error_others'):
        await call.answer('Thank you for feedback. We are improving our bot everyday! 🫰🏻')  



@dp.message(F.web_app_data)
async def webApp(message: types.Message):
    raw_data = message.web_app_data.data 

    try:
        data = json.loads(raw_data)

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        response_text = (f" Order received successfully!\n\n"
                         f"Name: {name}\n"
                         f"Email: {email}\n"
                         f"Phone: {phone}")
        await message.answer(response_text)
    except Exception as e:
        await message.answer(f"Received raw data: {raw_data}")


async def main():
    await dp.start_polling(bot)

if (__name__ == "__main__"):
    asyncio.run(main())