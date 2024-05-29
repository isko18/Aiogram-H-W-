from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('student.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS student(
    id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    direction VARCHAR(100),
    number VARCHAR(100)
);
""")

start_buttons = [
    types.KeyboardButton('Записаться'),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

courses = [
    "Backend",
    "Frontend",
    "Android",
    "IOS",
    "UX/UI",
    "Детское программирование",
    "Основы программирования"
]

courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
courses_keyboard.add(*courses)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    cursor.execute("SELECT id FROM student WHERE id = ?;", (message.from_user.id,))
    user_result = cursor.fetchone()
    if user_result is None:
        await message.reply(f'Здравствуйте, {message.from_user.full_name}!, Хотите записаться на DemoDay?', reply_markup=start_keyboard)
    else:
        await message.reply("Вы уже записаны")


@dp.message_handler(lambda message: message.text == 'Записаться')
async def sign_up(message: types.Message):
    cursor.execute("SELECT id FROM student WHERE id = ?;", (message.from_user.id,))
    user_result = cursor.fetchone()
    if user_result is None:
        await message.answer("Выберите направление:", reply_markup=courses_keyboard)
    else:
        await message.answer("Вы уже записаны")


@dp.message_handler(lambda message: message.text in courses)
async def choose_direction(message: types.Message):
    direction = message.text
    cursor.execute("SELECT id FROM student WHERE id = ?;", (message.from_user.id,))
    user_result = cursor.fetchone()
    if user_result is None:
        cursor.execute("INSERT INTO student (id, first_name, last_name, username, direction, number) VALUES (?, ?, ?, ?, ?, ?);",
                       (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, direction, ''))
        connection.commit()
        await message.answer("Вы выбрали направление: {}. Теперь введите ваш номер телефона:".format(direction))
    else:
        cursor.execute("UPDATE student SET direction = ? WHERE id = ?;", (direction, message.from_user.id))
        connection.commit()
        await message.answer(f"Ваше направление изменено на: {direction}")


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) >= 10)
async def get_phone_number(message: types.Message):
    phone_number = message.text
    cursor.execute("UPDATE student SET number = ? WHERE id = ?;", (phone_number, message.from_user.id))
    connection.commit()
    await message.answer("Вы успешно записались на DemoDay! Ваш номер телефона: {}".format(phone_number))


@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply('Я вас не понял')


executor.start_polling(dp, skip_updates=True)

