import telebot
import re
from telebot import types
import random
import time
markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
irregularV_list=types.KeyboardButton("Вывести список неправильных глаголов")
markup.add(irregularV_list)
irregularV_translate_help=types.KeyboardButton("Неправильный глагол по любой форме")
irregularV_practice=types.KeyboardButton("Режим тренировки (новое слово каждое нажатие)")
markup.add(irregularV_translate_help)
markup.add(irregularV_practice)
token="YOUR TOKEN"
bot = telebot.TeleBot(token)
vLineMatch = []
search_mode = {}
practice_mode = {}
print_mode = {}

current_verb = {}
correct_answer = {}

def findVerbStr(fname, v):
    pattern = re.compile(rf'(^|\s){re.escape(v)}(\s|$)', re.IGNORECASE)
    with open(fname, 'r', encoding='utf-8') as f:
        for line in f:
            if pattern.search(line):
                vLineMatch.append(line.strip())
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Привет! Я - телеграм-бот, который поможет запомнить неправильные глаголы в английском языке!", reply_markup=markup)
    search_mode[message.chat.id] = False
@bot.message_handler(content_types='text')
def reply_verbs(message):
    chat_id = message.chat.id
    if chat_id not in search_mode:
        search_mode[chat_id] = False
    if chat_id not in practice_mode:
        practice_mode[chat_id] = False
    if chat_id not in print_mode:
        print_mode[chat_id] = False
    if message.text=="Вывести список неправильных глаголов":
        with open('irrv1.txt', 'r', encoding='utf-8') as f:
            irrv_part1 = f.read()
        with open('irrv2.txt', 'r', encoding='utf-8') as f:
            irrv_part2 = f.read()
        with open('irrv3.txt', 'r', encoding='utf-8') as f:
            irrv_part3 = f.read()
        with open('irrv4.txt', 'r', encoding='utf-8') as f:
            irrv_part4 = f.read()
        if not practice_mode[chat_id]:
            print_mode[chat_id] = True
    if print_mode[chat_id]:
        if not practice_mode[chat_id]:
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
            print_mode[chat_id] = False
    elif message.text == "Неправильный глагол по любой форме":
        if not practice_mode[chat_id]:
            search_mode[chat_id] = True 
            practice_mode[chat_id] = False
            bot.send_message(chat_id, "Режим поиска включен. Введите слово для поиска:")
    
    elif message.text == "Режим тренировки (новое слово каждое нажатие)":

        search_mode[chat_id] = False
        print_mode[chat_id] = False
        practice_mode[chat_id] = True

        with open('irrv_onlyform', 'r', encoding='utf-8') as f:
            verbList = [line.strip() for line in f]

        rV = random.choice(verbList)
        current_verb[chat_id] = rV

        vLineMatch.clear()
        findVerbStr('irrv_no_tr.txt', rV)
        correct_answer[chat_id] = vLineMatch[0].lower()

        bot.send_message(chat_id, f"Введите все формы глагола {rV} в формате:\nV1 V2 V3 перевод")
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
    elif practice_mode[chat_id]:
        user_answer = message.text.strip().lower()
        right_answer = correct_answer.get(chat_id)

        if user_answer == right_answer:
            bot.send_message(chat_id, "Верно!")
            practice_mode[chat_id] = False
        else:
            bot.send_message(chat_id, f"Неверно.\nПравильный ответ: {right_answer}")
            practice_mode[chat_id] = False
    else:
        bot.send_message(chat_id, "Используйте кнопки для взаимодействия с ботом")
bot.polling()