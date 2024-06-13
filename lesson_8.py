# from aiogram import Bot, Dispatcher, types, executor
# from logging import basicConfig, INFO
# from dotenv import load_dotenv
# import os

# load_dotenv = ('.env')

# bot = Bot(os.environ.get('token'))
# dp = Dispatcher(bot)
# basicConfig(level=INFO)

# start_buttons = [
#     types.KeyboardButton("Отправить номер", request_contact = True),
#     types.KeyboardButton("Отправить локацию", request_location = True),   
# ]

# start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

# @dp.message_handler(commands='start')
# async def start(message:types.Message):
#     await message.answer(f"Привет {message.from_user.full_name}", reply_markup= start_keyboard)
    
# @dp.message_handler(content_types=types.ContentType.CONTACT)
# async def get_contact(message:types.Message):
#     print(message.contact.phone_number) #Номер телефона пользователя ТГ

# @dp.message_handler(content_types=types.ContentType.LOCATION)
# async def get_location(message:types.Message):
#     print(message.location) 
    
# inline = [
#     types.InlineKeyboardButton("О нас", callback_data='about_us'),
#     types.InlineKeyboardButton("Контакты", callback_data='contact'),
# ]  

# inline_keyboard = types.InlineKeyboardMarkup().add(*inline)

# @dp.message_handler(commands='help')
# async def help(message:types.Message):
#     await message.answer("Какую помощь вы хотите получить?", reply_markup=inline_keyboard)

# @dp.callback_query_handler(lambda call: call.data == 'about_us')
# async def about_us(message:types.Message):
#     await bot.send_message(message.from_user.id,"Geeks - это курсы программирования")
    
# @dp.callback_query_handler(lambda call: call.data == "contact")
# async def contact(message:types.Message):
#     await bot.send_message(message.from_user.id, "Нащи контакты\nАдрес: М.Аматова 1Б\nНомер телефона: 0505180600")


# executor.start_polling(dp, skip_updates=True)
