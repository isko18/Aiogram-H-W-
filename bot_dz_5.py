from aiogram import Dispatcher, types, Bot, executor
from bs4 import BeautifulSoup
import logging
import sqlite3
from config import token
import requests
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('new.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS news(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_text TEXT
            
)           
""")

connection.commit()
start_bottom = [
    types.KeyboardButton('news'),
    types.KeyboardButton('stop'),
    # types.KeyboardButton('news')
]
start_key = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_bottom)

class NewsState(StatesGroup):
    news_one = State()

@dp.message_handler(commands='start')
async def start(message: types.Message,state: FSMContext):
    # await NewsState.news_one.set()

    await message.reply(f'Привет {message.from_user.username}\nНовости>>>',reply_markup=start_key)

@dp.message_handler(text='news')
async def newses(message: types.Message):
    url = 'https://24.kg/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_news = soup.find_all('div', class_='title')
    
    for news_item in all_news:
        news_text = news_item.text
        await message.answer(news_text)
        cursor.execute("INSERT INTO news (news_text) VALUES (?)", (news_text,))
        connection.commit()
        await asyncio.sleep(2) 
        
        
@dp.message_handler(text='stop')
async def stop(message: types.Message):
    await message.reply('Бот остановлен.', reply_markup=types.ReplyKeyboardRemove())
    
    

    
    
executor.start_polling(dp, skip_updates=True)




