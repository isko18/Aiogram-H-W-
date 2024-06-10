from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from logging import basicConfig, INFO
import os, requests, asyncio, aioschedule, time

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
basicConfig(level=INFO)

async def get_btc_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')
    if price: 
        return f"Стоимость биткоина на {time.ctime()}, {price}$"
    else:
        return "Не удолось получить цену биткоина"
    
async def schedule():
    while monitoring:
        message = await get_btc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(1)
        
@dp.message_handler(commands=['start', 'help'])
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")
    
@dp.message_handler(commands='btc')
async def btc(message:types.Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    monitoring = True
    await message.answer("Начало мониторинга цены.")
    await schedule()

@dp.message_handler(commands='stop')
async def stop(message: types.Message):
    global monitoring
    monitoring = False
    await message.answer("Мониторинг цены остановлен.")
async def on(dp):
    aioschedule.every(1).seconds.do(schedule)
    
executor.start_polling(dp, on_startup=on ,skip_updates=True)

    
# @dp.message_handler(commands='BTC')
# async def get_btc_price(message:types.Message):
#     url = f"https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
#     responce = requests.get(url=url).json()
#     price = responce.get('price')
#     # await message.answer(f'{time.ctime()},{price}$')
#     if price:
#         return f"цена биткоина{price}"
#     else:
#         return f"не удалось"
# async def schedule():
#     while True:
#         message = await get_btc_price()
#         await bot.send_message(chat_id,message)

    
    # for i in range(10(price)):
    #     await message.answer(i)
    
    
executor.start_polling(dp,on_startup=on,skip_updates=True)
