import telebot
import re
from telebot import types
markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
irregularV_list=types.KeyboardButton("Вывести список неправильных глаголов")
markup.add(irregularV_list)
irregularV_translate_help=types.KeyboardButton("Неправильный глагол по любой форме")
markup.add(irregularV_translate_help)
token="YOUR TOKEN HERE"
bot = telebot.TeleBot(token)

search_mode = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Привет! Я - телеграм-бот, который поможет запомнить неправильные глаголы в английском языке!")
    search_mode[message.chat.id] = False
@bot.message_handler(commands=['verbs'])
def verbs_help(message):
    bot.send_message(message.chat.id,'Чем помочь?',reply_markup=markup)
    search_mode[message.chat.id] = False

@bot.message_handler(content_types='text')
def reply_verbs(message):
    chat_id = message.chat.id

    if chat_id not in search_mode:
        search_mode[chat_id] = False      
    if message.text=="Вывести список неправильных глаголов":
        with open('irrv1.txt', 'r', encoding='utf-8') as f:
            irrv_part1 = f.read()
        with open('irrv2.txt', 'r', encoding='utf-8') as f:
            irrv_part2 = f.read()
        with open('irrv3.txt', 'r', encoding='utf-8') as f:
            irrv_part3 = f.read()
        with open('irrv4.txt', 'r', encoding='utf-8') as f:
            irrv_part4 = f.read()   
        if not irrv_part1:
            bot.send_message(message.chat.id, 'Список - часть 1 отсутствует')
        else:
            bot.send_message(message.chat.id, irrv_part1)
        if not irrv_part2:
            bot.send_message(message.chat.id, 'Список - часть 2 отсутствует')
        else:
            bot.send_message(message.chat.id, irrv_part2)
        if not irrv_part3:
            bot.send_message(message.chat.id, 'Список - часть 3 отсутствует')
        else:
            bot.send_message(message.chat.id, irrv_part3)
        if not irrv_part4:
            bot.send_message(message.chat.id, 'Список - часть 4 отсутствует')
        else:
            bot.send_message(message.chat.id, irrv_part4)
    elif message.text == "Неправильный глагол по любой форме":
        search_mode[chat_id] = True 
        bot.send_message(chat_id, "Режим поиска включен. Введите слово для поиска:")
        query = message.text.strip().lower()
    elif search_mode[chat_id]:
        query = message.text.strip().lower()
        if not query:
            return
        found_lines = []
        files = ['irrv1.txt', 'irrv2.txt', 'irrv3.txt', 'irrv4.txt']

        pattern = re.compile(rf'(^|\s){re.escape(query)}(\s|$)', re.IGNORECASE)

        for filename in files:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    for line in f:
                        if pattern.search(line):
                            found_lines.append(line.strip())
            except FileNotFoundError:
                continue

        if found_lines:
            result_text = "Найдено:\n" + "\n".join(found_lines)
            for chunk in [result_text[i:i+4000] for i in range(0, len(result_text), 4000)]:
                bot.send_message(message.chat.id, chunk)
        else:
            bot.send_message(message.chat.id, "Ничего не найдено. Попробуй другое слово.")
    else:
        bot.send_message(chat_id, "Используйте кнопки для взаимодействия с ботом")
bot.polling()





