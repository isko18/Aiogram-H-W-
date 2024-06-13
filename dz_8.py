import smtplib
from aiogram import Dispatcher, executor, Bot, types
from config import TOKEN, SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
from email.message import EmailMessage
from logging import basicConfig, INFO
from dotenv import load_dotenv
import os
import random

load_dotenv('.env')

def send_verification_code(email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Ваш код верификации'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f'Ваш код верификации: {code}')
    
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
basicConfig(level=INFO)

verification_codes = {}

inline = types.InlineKeyboardButton('Идентификация', callback_data='about_us')
i_inline = types.InlineKeyboardMarkup().add(inline)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=i_inline)
    
@dp.callback_query_handler(lambda call: call.data == 'about_us')
async def about_us(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите свой email")

@dp.message_handler(lambda message: message.text and "@" in message.text)
async def process_email(message: types.Message):
    email = message.text
    code = ''.join(random.choices('0123456789', k=6))
    verification_codes[message.from_user.id] = code
    send_verification_code(email, code)
    await bot.send_message(message.from_user.id, "Введите полученный код для завершения верификации.")

@dp.message_handler(lambda message: message.text.isdigit())
async def process_verification_code(message: types.Message):
    code = message.text
    if message.from_user.id in verification_codes and verification_codes[message.from_user.id] == code:
        await bot.send_message(message.from_user.id, "Вы успешно идентифицировались!")
    else:
        await bot.send_message(message.from_user.id, "Неправильный ввод. Пожалуйста, попробуйте еще раз.")

executor.start_polling(dp, skip_updates=True)
