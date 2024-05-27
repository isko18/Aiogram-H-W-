import sqlite3, logging, time
from config import token
from aiogram import Dispatcher, types, Bot, executor
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('banc_users.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS banc_users(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    direction VARCHAR(100),
    number VARCHAR(100)
);
""")

@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    cursor.execute(f'SELECT id FROM banc_users WHERE id = {message.from_user.id}')
    user_result = cursor.fetchall()
    if not user_result:
        await message.answer('Приве пожалуста зарегистрируйтесь написав /registr')
    else:
        await message.answer('Привет! Вы уже зарегистрированы.')

class MallingState(StatesGroup):
    text = State()

@dp.message_handler(commands='registr')
async def start_registr(message: types.Message):
    await message.answer("Напишите своё: Имя, Фамилия, Никнейм, Направление, номер телефона через запятую")
    await MallingState.text.set()

@dp.message_handler(state=MallingState.text)
async def send_malling(message: types.Message, state: FSMContext):
    await message.answer("Начинаю регистрацию....")
    data = message.text.split(',')
    if len(data) == 5:
        cursor.execute("INSERT INTO banc_users (id, first_name, last_name, username, direction, number) VALUES (?, ?, ?, ?, ?, ?);",
                       (message.from_user.id,
                        message.from_user.first_name,
                        message.from_user.last_name,
                        message.from_user.username,
                        data[3].strip(),
                        data[4].strip()))
        connection.commit()
        await message.answer('Регистрация успешно завершена!')
    else:
        await message.answer('Если ошибка то убедитесь что пишите с запятыми.')
    await state.finish()

@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp, skip_updates=True)
