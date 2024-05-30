import sqlite3
import logging
from config import token
from aiogram import Dispatcher, types, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('user.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    user_name VARCHAR(100),
    direction VARCHAR(100),
    number INTEGER NOT NULL DEFAULT 996
)
""")
connection.commit()

start_buttons = [
    types.KeyboardButton('Backend'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Детское программирование'),
    types.KeyboardButton('Основы программирования'),
    types.KeyboardButton('Оставить заявку'),
    types.KeyboardButton('Ios'),
    types.KeyboardButton('Назад')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    user_result = cursor.fetchall()
    if not user_result:
        cursor.execute("INSERT INTO users (id, first_name, last_name, user_name) VALUES (?, ?, ?, ?);",
                       (user_id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
        connection.commit()
    
    await message.reply(f'Приветствую, {message.from_user.full_name}! Приглашаю вас посетить Demoday в Geeks. Вот наши направления:', reply_markup=start_keyboard)

async def request_contact(message: types.Message, direction: str):
    botom = types.KeyboardButton("Это хочу:)", request_contact=True)
    bottom = types.ReplyKeyboardMarkup(resize_keyboard=True).add(botom)
    await message.answer(f'Вы выбрали {direction}. Подтвердить:', reply_markup=bottom)
    
    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def get_contact(message: types.Message):
        cursor.execute("UPDATE users SET direction = ?, number = ? WHERE id = ?",
                       (direction, message.contact.phone_number, message.from_user.id))
        connection.commit()
        await message.answer("Вы успешно записались на курс :)")
        await bot.send_message(-1002179629908, f"Заявка на курсы:\nИмя: {message.contact.first_name}\nФамилия: {message.contact.last_name}\nНомер телефона: {message.contact.phone_number}")

@dp.message_handler(text='Backend')
async def choose_backend(message: types.Message):
    await request_contact(message, "Backend")

@dp.message_handler(text='Android')
async def choose_android(message: types.Message):
    await request_contact(message, "Android")

@dp.message_handler(text='UX/UI')
async def choose_ux_ui(message: types.Message):
    await request_contact(message, "UX/UI")

@dp.message_handler(text='Frontend')
async def choose_frontend(message: types.Message):
    await request_contact(message, "Frontend")

@dp.message_handler(text='Ios')
async def choose_ios(message: types.Message):
    await request_contact(message, "Ios")

@dp.message_handler(text='Детское программирование')
async def choose_child_programming(message: types.Message):
    await request_contact(message, "Детское программирование")

@dp.message_handler(text='Основы программирования')
async def choose_basic_programming(message: types.Message):
    await request_contact(message, "Основы программирования")

@dp.message_handler(text="Назад")
async def back_start(message: types.Message):
    await start(message)

class MallingState(StatesGroup):
    text = State()

@dp.message_handler(commands='malling')
async def start_malling(message: types.Message):
    await message.answer("Напишите текст для рассылки: ")
    await MallingState.text.set()


@dp.message_handler(state=MallingState.text)
async def send_malling(message: types.Message, state: FSMContext):
    await message.answer("Начинаю рассылку....")
    cursor.execute("SELECT id FROM users;")
    users_id = cursor.fetchall()
    for user_id in users_id:
        await bot.send_message(user_id[0], message.text)
    await message.answer('Рассылка окончена...')
    await state.finish()

@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp, skip_updates=True)
