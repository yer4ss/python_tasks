import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])             #салам кидает
def message_start_emae(message):
   user_name = message.from_user.first_name
   bot.send_message(message.chat.id, "Хэллоу пипл! Че как, вазап " + user_name + "?\n"
                                       "Если канкретно пообщаться желание крейзи, то /text в помощь.\n"
                                       "Ну или стикерсы покидай - /sticker.\n"
                                       "Йоу хоуми, настрочи там в ловер /help, если сомтинг надо будет.")


@bot.message_handler(commands=['help'])              #поддержка делает
def message_help_emae(message):
   bot.send_message(message.chat.id, "Че там бро, выкладывай, что ю нид?\n"
                                       "Иф ю нид мор инфо, тогда ин ловер /info.\n"
                                       "Настрочи /start, иф ю нид старт сначала.\n"
                                       "Элс, закрой бота, ибо ай донт ноу, что ю нид фром ми - /close.")


@bot.message_handler(commands=['info'])              #информбюро
def message_info_emae(message):
   bot.send_message(message.chat.id, "Йоу, бро, вот инфа ту ю:\n"
                                       "Зис бот креатед фор теститнг май бэтэр инглиш йоу\n"
                                       "Иф сомтинг случится, строчи в ловер /help, и я хелпинг фо ю бро.")


@bot.message_handler(commands=['close'])             #закрывает бота
def message_close_emae(message):
   bot.send_message(message.chat.id, "Давай, бро, иф ю нид ми, я алвейс на связи.\n"
                                       "Обнял, поднял, руку пожал, в щечку поцеловал, пульс давление проверил, салам кинул!")


@bot.message_handler(commands=['sticker'])           #присылает стикер
def message_sticker_emae(message):
   sticker_id = "CAACAgIAAxkBAAIBdWe0DxugZsdUCrCoBpcDY3ZEKcpkAAKrWwACTeCgSaHvF_bPi83NNgQ"
   bot.send_sticker(message.chat.id, sticker_id)


@bot.message_handler(content_types=['text'])         #общение
def message_beseda_emae(message):

   user_text = message.text

   if user_text == "Привет":
      bot.send_message(message.chat.id, "Вечер в хату!\n"
                                          "Код ис воркинг, хэлпуй дальше - /help.")
   elif user_text == "Салам":
      bot.send_message(message.chat.id, "Уагалейкум, брат!\n"
                                          "Код ис воркинг, хэлпуй дальше - /help.")
   elif user_text == "Хеллоу":
      bot.send_message(message.chat.id, "Ваазаааааап, брооооооо!\n"
                                          "Код ис воркинг, хэлпуй дальше - /help.")
   else:
      bot.send_message(
         message.chat.id, 
         "Поздоровайся нормально да, бъютифул сделай канкретно.\n"
         "Иф в край не получается, клик ту готовый ансвер емае /help."
      )


@bot.message_handler(content_types=['sticker'])      #повторяет стикер
def message_sticker_emae(message):
   sticker_id = message.sticker.file_id
   bot.send_sticker(message.chat.id, sticker_id)


# @bot.message_handler(content_types=['sticker'])     #айдишник стикера
# def sticker_id(message):
#    sticker_id = message.sticker.file_id  # Получаем file_id стикера
#    print(f"{sticker_id}")  # Выводим в консоль
#    bot.send_message(message.chat.id, f"Sticker ID: `{sticker_id}`", parse_mode="Markdown")  # Отправляем пользователю


@bot.message_handler(content_types=['photo'])        #сохраняет фото
def message_photo_emae(message):
   try:
      file_info = bot.get_file(message.photo[-1].file_id)
      downloaded_file = bot.download_file(file_info.file_path)
      src = "A:\yer4ss\Work\im python\photos"
      with open(src, 'wb') as new_file:
         new_file.write(downloaded_file)
      bot.reply_to(message, "Пхото сэйвед")
   except Exception as e:
      bot.reply_to(message, e)



#пусть бот отправляет /секретный файл и к нему прикрепляет фото

# @bot.message_handler(commands=['secret_file'])        #отправляет файл
# def message_secret_file_emae(message):
#    doc = open("A:\yer4ss\Work\im python\secret.txt", "rb")
#    bot.send_document(message.chat.id, doc)
#    bot.send_message(message.chat.id, "Секретный файл отправлен")


if __name__ == "__main__":
   bot.infinity_polling()