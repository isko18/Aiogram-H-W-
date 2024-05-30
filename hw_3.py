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


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    user_name VARCHAR(100),
    direction VARCHAR(100),
    number VARCHAR(20) NOT NULL DEFAULT '996'
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
    user_result = cursor.fetchone()
    if not user_result:
        cursor.execute("INSERT INTO users (id, first_name, last_name, user_name) VALUES (?, ?, ?, ?);",
                       (user_id, message.from_user.first_name, message.from_user.last_name, message.from_user.username))
        connection.commit()
    
    await message.reply(f'Приветствую, {message.from_user.full_name}! Приглашаю вас посетить Demoday в Geeks. Вот наши направления:', reply_markup=start_keyboard)


async def request_contact(message: types.Message, direction: str):
    botom = types.KeyboardButton("Это хочу:)", request_contact=True)
    back_button = types.KeyboardButton("Назад")
    bottom = types.ReplyKeyboardMarkup(resize_keyboard=True).add(botom, back_button)
    await message.answer(f'Вы выбрали {direction}. Подтвердить:', reply_markup=bottom)


class Form(StatesGroup):
    direction = State()


@dp.message_handler(text='Backend')
async def course_backend(message: types.Message):
    await message.reply("Backend - это серверная сторона сайта или приложения. Вы научитесь создавать серверы, работать с базами данных и обеспечивать безопасность данных.")

@dp.message_handler(text='Android')
async def course_android(message: types.Message):
    await message.reply("Android - это разработка мобильных приложений для операционной системы Android. Вы научитесь создавать приложения на Java и Kotlin.")

@dp.message_handler(text='UX/UI')
async def course_ux_ui(message: types.Message):
    await message.reply("UX/UI - это дизайн пользовательского интерфейса и опыта. Вы научитесь создавать удобные и красивые интерфейсы для сайтов и приложений.")

@dp.message_handler(text='Frontend')
async def course_frontend(message: types.Message):
    await message.reply("Frontend - это лицевая сторона сайта или приложения. Вы научитесь создавать динамичные и интерактивные веб-страницы с помощью HTML, CSS и JavaScript.")

@dp.message_handler(text='Ios')
async def course_ios(message: types.Message):
    await message.reply("iOS - это разработка мобильных приложений для операционной системы iOS. Вы научитесь создавать приложения на Swift и Objective-C.")


@dp.message_handler(text='Детское программирование')
async def course_child_programming(message: types.Message):
    await message.reply("Детское программирование - это изучение основ программирования для детей. Дети научатся основам алгоритмов и логики, создавая простые программы.")

@dp.message_handler(text='Основы программирования')
async def course_basic_programming(message: types.Message):
    await message.reply("Основы программирования - это объяснение базовых концепций программирования для взрослых. Вы научитесь основам алгоритмов и синтаксису популярных языков программирования.")

@dp.message_handler(text='Оставить заявку')
async def leave_application(message: types.Message):
    confirm_buttons = [
        types.KeyboardButton('Backend'),
        types.KeyboardButton('Android'),
        types.KeyboardButton('Frontend'),
        types.KeyboardButton('UX/UI'),
        types.KeyboardButton('Детское программирование'),
        types.KeyboardButton('Основы программирования'),
        types.KeyboardButton('Ios'),
        types.KeyboardButton('Назад')
    ]
    confirm_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*confirm_buttons)
    await message.reply("Выберите направление для заявки:", reply_markup=confirm_keyboard)
    await Form.direction.set()

@dp.message_handler(state=Form.direction)
async def choose_direction(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await start(message)
        await state.finish()
        return
    direction = message.text
    await state.update_data(direction=direction)
    await request_contact(message, direction)

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.direction)
async def handle_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    direction = user_data.get('direction', 'Не указано')

    cursor.execute("UPDATE users SET direction = ?, number = ? WHERE id = ?",
                   (direction, message.contact.phone_number, user_id))
    connection.commit()
    await message.answer("Вы успешно записались на курс :)")
    await bot.send_message(-4269502098, f"Заявка на курсы:\nИмя: {message.contact.first_name}\nФамилия: {message.contact.last_name}\nНомер телефона: {message.contact.phone_number}")
    await state.finish()


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
