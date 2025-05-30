import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
import requests
import time


bot = telebot.TeleBot('7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng')
api_key = '17697edb22cd6287f4a12ccb3e497513'


cities = [
   "Петропавловск", "Кокшетау", "Костанай", "Астана",
   "Шымкент", "Тараз", "Кызылорда", "Туркестан", "Алматы",
   "Атырау", "Уральск", "Актау", "Актобе",
   "Усть-Каменогорск", "Семей", "Павлодар",
   "Караганда", "Темиртау", "Талдыкорган"
]

city_info = {
   "Астана": ("Столица Казахстана, известная своей современной архитектурой. Город знаменит своими футуристическими зданиями, такими как Байтерек, Хан Шатыр и Дворец мира и согласия. В Астане проходят важные экономические и культурные форумы мирового уровня. Зимой город превращается в снежную сказку, а летом привлекает гостей своими зелёными парками."),
   "Алматы": ("Крупнейший город Казахстана, окружённый живописными горами Заилийского Алатау. Известен как культурный и финансовый центр страны. Здесь расположены знаменитый высокогорный каток Медео, горнолыжный курорт Шымбулак и смотровая площадка Кок-Тобе. Алматы славится своими зелёными улицами, уютными кафе и богатой историей."),
   "Шымкент": ("Третий по величине город Казахстана, известный своими восточными базарами, гостеприимством и богатой историей. Основанный более 2 200 лет назад, он является одним из древнейших городов региона. Здесь можно посетить этнографический комплекс «Кен-Баба», медресе XIX века и Археологический музей."),
   "Кокшетау": ("Живописный город, окружённый озёрами и лесами. Кокшетау славится своими курортными зонами, такими как Бурабай и Зеренда, привлекающими туристов круглый год. Бурабай часто называют \"Казахстанской Швейцарией\" из-за его горных пейзажей и чистых озёр."),
   "Костанай": ("Город с богатым культурным наследием, расположенный на севере Казахстана. Здесь можно найти исторические памятники, музеи и театры. В регионе развита сельскохозяйственная и промышленная отрасль. В Костанае также проходит ежегодный фестиваль «Тобол-фест», посвящённый народным традициям."),
   "Петропавловск": ("Один из старейших городов Казахстана, основанный в XVIII веке. Здесь сохранилось множество архитектурных памятников, включая Петропавловскую крепость. Город известен своими уютными набережными, а также музеем литературы и искусства, посвящённым творчеству казахских писателей."),
   "Тараз": ("Один из древнейших городов Центральной Азии с историей более 2 000 лет. Тараз славится древними мавзолеями Карахана и Айша-биби, которые являются важными культурными памятниками. Город также называют 'колыбелью казахской цивилизации' за его археологическое и историческое значение."),
   "Кызылорда": ("Город на реке Сырдарья, исторический центр Казахстана. Здесь в XIX веке располагалась первая столица Казахской АССР. Кызылорда также известна как центр казахской национальной письменности и образования, а поблизости находится знаменитый космодром Байконур."),
   "Туркестан": ("Один из самых древних и священных городов Казахстана. Здесь находится мавзолей Ходжи Ахмеда Ясави – объект Всемирного наследия ЮНЕСКО. Туркестан является духовным и культурным центром страны, ежегодно привлекающим тысячи паломников и туристов."),
   "Атырау": ("Нефтяная столица Казахстана, расположенная на реке Урал. Город разделён на две части, европейскую и азиатскую. Атырау известен своими рыбными промыслами, нефтяными месторождениями и современными небоскрёбами."),
   "Уральск": ("Исторический город на западе Казахстана, основанный в XVI веке. Уральск славится своей старинной архитектурой, особенно Казанским собором и домом Пугачёва. Здесь можно посетить музеи, посвящённые истории казачества и древнего Золотого Орды."),
   "Актау": ("Город у Каспийского моря с красивыми пляжами и скалистыми пейзажами. Является важным портовым и туристическим центром. Вблизи города можно посетить урочище Босжира и подземную мечеть Бекет-Ата, считающуюся святыней."),
   "Актобе": ("Динамично развивающийся город на западе Казахстана. Здесь расположены крупные металлургические заводы и современные торговые центры. В окрестностях города можно посетить уникальные геологические образования – меловые горы Актау."),
   "Усть-Каменогорск": ("Город металлургов, расположенный среди гор Восточного Казахстана. Он известен своими красивыми природными пейзажами, такими как Бухтарминское водохранилище и национальный парк Катон-Карагай."),
   "Семей": ("Исторический город, связанный с именем Абая Кунанбаева. В Семее расположен музей Абая, старейшая мечеть Казахстана и мост через Иртыш – один из самых длинных в Центральной Азии."),
   "Павлодар": ("Город с развитой промышленностью и живописными набережными. Павлодар известен своими современными театрами, музеями и близостью к национальному парку Баянаул."),
   "Караганда": ("Крупный промышленный центр Казахстана, связанный с угольной промышленностью. Город славится своим театром имени Станиславского и парком Ботанический сад. Недалеко находится музей ГУЛАГа в поселке Долинка."),
   "Темиртау": ("Город металлургов, важный центр чёрной металлургии Казахстана. Здесь находится крупнейший металлургический завод страны. Также город известен своим ледовым дворцом и живописной набережной реки Нура."),
   "Талдыкорган": ("Административный центр Жетысуской области. Город славится своим живописным расположением у подножия гор Жетысуского Алатау. Здесь находится монумент Бабаларға тағзым, посвящённый предкам, а также парк Первого Президента и современный культурный центр. Талдыкорган — это уютный город с развитой инфраструктурой и красивыми природными окрестностями.")
}

city_images = {
   "Астана": "A:/yer4ss/Work/im python/bot gid/images/Астана.jpg",
   "Алматы": "A:/yer4ss/Work/im python/bot gid/images/Алматы.jpg",
   "Шымкент": "A:/yer4ss/Work/im python/bot gid/images/Шымкент.jpg",
   "Кокшетау": "A:/yer4ss/Work/im python/bot gid/images/Кокшетау.jpg",
   "Костанай": "A:/yer4ss/Work/im python/bot gid/images/Костанай.jpg",
   "Петропавловск": "A:/yer4ss/Work/im python/bot gid/images/Петропавловск.jpg",
   "Тараз": "A:/yer4ss/Work/im python/bot gid/images/Тараз.jpg",
   "Кызылорда": "A:/yer4ss/Work/im python/bot gid/images/Кызылорда.jpg",
   "Туркестан": "A:/yer4ss/Work/im python/bot gid/images/Туркестан.jpg",
   "Атырау": "A:/yer4ss/Work/im python/bot gid/images/Атырау.jpg",
   "Уральск": "A:/yer4ss/Work/im python/bot gid/images/Уральск.jpg",
   "Актау": "A:/yer4ss/Work/im python/bot gid/images/Актау.jpg",
   "Актобе": "A:/yer4ss/Work/im python/bot gid/images/Актобе.jpg",
   "Усть-Каменогорск": "A:/yer4ss/Work/im python/bot gid/images/Усть-Каменогорск.jpg",
   "Семей": "A:/yer4ss/Work/im python/bot gid/images/Семей.jpg",
   "Павлодар": "A:/yer4ss/Work/im python/bot gid/images/Павлодар.jpg",
   "Караганда": "A:/yer4ss/Work/im python/bot gid/images/Караганда.jpg",
   "Темиртау": "A:/yer4ss/Work/im python/bot gid/images/Темиртау.jpg",
   "Талдыкорган": "A:/yer4ss/Work/im python/bot gid/images/Талдыкорган.jpg"
}

city_maps = {
   "Астана": "https://www.google.com/maps/search/?q=Астана&hl=ru",
   "Алматы": "https://www.google.com/maps/search/?q=Алматы&hl=ru",
   "Шымкент": "https://www.google.com/maps/search/?q=Шымкент&hl=ru",
   "Кокшетау": "https://www.google.com/maps/search/?q=Кокшетау&hl=ru",
   "Костанай": "https://www.google.com/maps/search/?q=Костанай&hl=ru",
   "Петропавловск": "https://www.google.com/maps/search/?q=Петропавловск&hl=ru",
   "Тараз": "https://www.google.com/maps/search/?q=Тараз&hl=ru",
   "Кызылорда": "https://www.google.com/maps/search/?q=Кызылорда&hl=ru",
   "Туркестан": "https://www.google.com/maps/search/?q=Туркестан&hl=ru",
   "Атырау": "https://www.google.com/maps/search/?q=Атырау&hl=ru",
   "Уральск": "https://www.google.com/maps/search/?q=Уральск&hl=ru",
   "Актау": "https://www.google.com/maps/search/?q=Актау&hl=ru",
   "Актобе": "https://www.google.com/maps/search/?q=Актобе&hl=ru",
   "Усть-Каменогорск": "https://www.google.com/maps/search/?q=Усть-Каменогорск&hl=ru",
   "Семей": "https://www.google.com/maps/search/?q=Семей&hl=ru",
   "Павлодар": "https://www.google.com/maps/search/?q=Павлодар&hl=ru",
   "Караганда": "https://www.google.com/maps/search/?q=Караганда&hl=ru",
   "Темиртау": "https://www.google.com/maps/search/?q=Темиртау&hl=ru",
   "Талдыкорган": "https://www.google.com/maps/search/?q=Талдыкорган&hl=ru"
}


@bot.message_handler(commands=['help'])
def help(message):
   bot.send_message(message.chat.id, 
                     "<b>Мои команды:</b>\n"
                     "/start — начать общение с ботом\n"
                     "/help — получить справку о боте\n"
                     "/about — узнать информацию о разработчике\n"
                     "/stop — завершить общение с ботом", parse_mode='html')

@bot.message_handler(commands=['about'])
def about(message):
   bot.send_message(message.chat.id, 
                     "Этот бот был создан в рамках проекта по изучению Python и Telegram API.\n"
                     "Разработчик: <em><b>yerazz</b></em>", parse_mode='html')

@bot.message_handler(commands=['stop'])
def stop(message):

   # chat_id = message.chat.id
   # for i in range(message.message_id - 20, message.message_id + 1):
   #    try:
   #       bot.delete_message(chat_id, i)
   #    except Exception as e:
   #       print(f"Не удалось удалить сообщение {i}: {e}")

   bot.send_message(message.chat.id, "До свидания! Бот остановлен и больше не реагирует на сообщения.")
   os._exit(0)

@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.chat.id, 
                     f"Привет, {message.from_user.first_name}! 👋\n"
                     "Я - твой персональный гид по Казахстану! 🇰🇿\n"
                     "Могу показать тебе интересные места, рассказать факты и подсказать погоду. 🌍✨")

   command_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   command_markup.row('/start', '/stop')
   command_markup.row('/help', '/about')

   inline_markup = types.InlineKeyboardMarkup()
   btn1 = types.InlineKeyboardButton('Выбрать город', callback_data='select_city')
   btn2 = types.InlineKeyboardButton('Ввести название', callback_data='input_city')
   inline_markup.row(btn1, btn2)

   bot.send_message(message.chat.id, "Для начала выбери действие:",  reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(callback):
   if callback.data == 'select_city':
      markup = types.InlineKeyboardMarkup()
      for city in cities:
         markup.add(InlineKeyboardButton(city, callback_data=city))
      bot.send_message(callback.message.chat.id, "Выбери город из списка:", reply_markup=markup)
   elif callback.data == 'input_city':
      bot.send_message(callback.message.chat.id, "Введите название города:")
   # elif callback.data in cities:
   #    city = callback.data
   #    bot.send_message(callback.message.chat.id, f"Информация о городе {city}:\n{city_info[city]}")
   #    bot.send_photo(callback.message.chat.id, open(city_images[city], 'rb'))
   #    bot.send_message(callback.message.chat.id, f"Посмотреть на карте: {city_maps[city]}")

bot.polling(none_stop=True)




# import telebot
# import webbrowser
# from telebot import types
# import os

# bot = telebot.TeleBot('7780668347:AAFTwSbXzNg02naVu_g2x-k2GiPiYPVlOng')
# # api_key = '17697edb22cd6287f4a12ccb3e497513'

# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup()                                             # кнопки под клавой
#     btn1 = types.KeyboardButton('/start')
#     btn2 = types.KeyboardButton('/help')
#     btn3 = types.KeyboardButton('/about')
#     btn4 = types.KeyboardButton('/map')
#     markup.row(btn1, btn2, btn3)
#     markup.add(btn4)

#     bot.send_message(message.chat.id, 'Hello', reply_markup=markup)


#     markup = types.InlineKeyboardMarkup()                                             # кнопки под сообщением
#     markup.add(types.InlineKeyboardButton('Google', url='https://www.google.com'))
#     markup.add(types.InlineKeyboardButton('wasd', callback_data='wasd'))             # callback вызывает функцию  

#     btn2 = types.InlineKeyboardButton('edit', callback_data='edit_text')
#     btn3 = types.InlineKeyboardButton('delete', callback_data='delete_text')
#     markup.row(btn2, btn3)                                                      # создает кнопки в одну строку   

#     bot.send_message(message.chat.id, 'text', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)       # обрабатывает кнопку, lambda - анонимная функция
# def callback_nahuy(callback):
#     if callback.data == 'wasd':
#         bot.send_message(callback.message.chat.id, 'wasd')
#     elif callback.data == 'edit_text':
#         bot.edit_message_text('edited', callback.message.chat.id, callback.message.message_id)
#     elif callback.data == 'delete_text':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)   # удаляет предпоследнее сообщение в чате


# @bot.message_handler(commands=['help'])
# def help(message):
#     bot.send_message(message.chat.id, '<b>I</b> <em>can help</em> <u>you</u>!', parse_mode='html')


# @bot.message_handler(commands=['about'])
# def about(message):
#     bot.send_message(message.chat.id, message)


# @bot.message_handler(commands=['map', 'location'])                 # открывает карту
# def map(message):
#     webbrowser.open('https://www.google.com/maps')


# @bot.message_handler(commands=['stop'])
# def stop(message):
#     chat_id = message.chat.id

#     # Удаляем последние 20 сообщений (можно увеличить)
#     for i in range(message.message_id - 20, message.message_id + 1):
#         try:
#             bot.delete_message(chat_id, i)
#         except Exception as e:
#             print(f"Не удалось удалить сообщение {i}: {e}")

#     bot.send_message(chat_id, "До свидания! Если захочешь поговорить, пиши /start.")
#     os._exit(0)


# @bot.message_handler(content_types=['text'])             # обрабатывает сообщения простым текстом
# def text(message):
#     if message.text.lower() == 'hello':
#         bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!')
#     elif message.text.lower() == 'bye':
#         bot.send_message(message.chat.id, f'Bye, {message.from_user.first_name}!')


# bot.polling(none_stop=True)