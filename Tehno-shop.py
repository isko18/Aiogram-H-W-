from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from logging import basicConfig, INFO
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Товары'),
    types.KeyboardButton('Заказать'),
    types.KeyboardButton('Контакты'),
]

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

class OrderForm(StatesGroup):
    waiting_for_articul = State()
    waiting_for_contact = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=start_keyboard)

@dp.message_handler(text='О нас')
async def about_us(message: types.Message):
    await message.reply("Tehno-shop - Это магазин смартфонов. Мы открылись в 2024г в городе Ош. В нашем магазине вы можете приобрести смартфон любой модели: iPhone, Samsung, Redmi и другие.")

product_buttons = [
    types.KeyboardButton("Samsung"),
    types.KeyboardButton("iPhone"),
    types.KeyboardButton("Redmi"),
    types.KeyboardButton("Назад")
]
product_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*product_buttons)

@dp.message_handler(text='Товары')
async def all_goods(message: types.Message):
    await message.answer("Вот наши товары", reply_markup=product_keyboard)

@dp.message_handler(text='Samsung')
async def samsung_info(message: types.Message):
    await message.answer_photo('https://3dnews.ru/assets/external/illustrations/2023/05/17/1086907/sm.06.800.jpg')
    await message.reply("Samsung - A54\nЦена - 50000\nАртикул - 13\nПамять - 240GB\nЦвет: черный")

@dp.message_handler(text='Redmi')
async def redmi_info(message: types.Message):
    await message.answer_photo('https://login.kg/image/cache/webp/catalog/new/Phones/Xiaomi/Note%2012%20Pro/1-500x400.webp')
    await message.reply("Redmi - Note 8\nЦена - 10000\nАртикул - 15\nПамять - 32GB\nЦвет: белый")

@dp.message_handler(text='iPhone')
async def iphone_info(message: types.Message):
    await message.answer_photo('https://ipiter.ru/upl/modules/shop/360/2q29vzo5ry.jpg')
    await message.reply("iPhone - 15 Pro Max\nЦена - 155900\nАртикул - 56\nПамять - 1TB\nЦвет: черный")

@dp.message_handler(text="Назад")
async def back_to_start(message: types.Message):
    await message.reply("Вы вернулись в главное меню", reply_markup=start_keyboard)

@dp.message_handler(text='Заказать')
async def order(message: types.Message):
    await message.reply("Пожалуйста, введите артикул товара, который хотите заказать:")
    await OrderForm.waiting_for_articul.set()

@dp.message_handler(state=OrderForm.waiting_for_articul)
async def process_articul(message: types.Message, state: FSMContext):
    await state.update_data(articul=message.text)
    await message.reply("Пожалуйста, поделитесь вашим контактом", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Поделиться контактом", request_contact=True)))
    await OrderForm.waiting_for_contact.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=OrderForm.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    articul = user_data['articul']
    contact = message.contact.phone_number
    user_name = message.contact.full_name

    order_message = f"Новый заказ!\nАртикул: {articul}\nКонтакт: {contact}\nИмя: {user_name}"
    await bot.send_message(chat_id=-4269502098, text=order_message)

    await message.reply("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.", reply_markup=start_keyboard)
    await state.finish()


@dp.message_handler(text='Контакты')
async def send_contact(message: types.Message):
    await message.answer(f'{message.from_user.full_name}, вот наши контакты:')
    await message.answer_contact(phone_number="+996504736767", first_name="Tehno-shop")



executor.start_polling(dp, skip_updates=True)