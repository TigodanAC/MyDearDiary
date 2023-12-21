﻿import telebot
from telebot import types

TOKEN = '6662823857:AAERFYvIoJGWreU7_y80R_USjUlWghILRFM'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       row_width=3)
    item_1 = types.KeyboardButton(text="Дневник")
    item_2 = types.KeyboardButton(text="Досуг")
    item_3 = types.KeyboardButton(text="Счётчик калорий")
    markup.add(item_1, item_2, item_3)
    bot.send_message(message.chat.id,
                     "Привет, я твой дорогой дневник! С моей помощью ты можешь создавать записи в виртуальный дневник, "
                     "искать книги/сериалы/фильмы для досуга, а также считать калории!",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Дневник":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=5)
        item_1 = types.KeyboardButton(text="Добавить запись")
        item_2 = types.KeyboardButton(text="Прочесть запись")
        item_3 = types.KeyboardButton(text="Вывести все записи")
        item_4 = types.KeyboardButton(text="Удалить запись")
        item_5 = types.KeyboardButton(text="Назад")
        markup.add(item_1, item_2, item_3, item_4, item_5)
        bot.reply_markup = markup
        bot.send_message(message.chat.id, "Я к Вашим услугам!", reply_markup=markup)
    elif message.text == "Досуг":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=4)
        item_1 = types.KeyboardButton(text="Найти фильм")
        item_2 = types.KeyboardButton(text="Найти сериал")
        item_3 = types.KeyboardButton(text="Найти книгу")
        item_4 = types.KeyboardButton(text="Списки")
        item_5 = types.KeyboardButton(text="Назад")
        markup.add(item_1, item_2, item_3, item_4, item_5)
        bot.send_message(message.chat.id, "Я к Вашим услугам!", reply_markup=markup)
    elif message.text == "Счётчик калорий":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=5)
        item_1 = types.KeyboardButton(text="Добавить блюдо")
        item_2 = types.KeyboardButton(text="Найти блюдо")
        item_3 = types.KeyboardButton(text="Списки блюд")
        item_4 = types.KeyboardButton(text="Cчётчик")
        item_5 = types.KeyboardButton(text="Назад")
        markup.add(item_1, item_2, item_3, item_4, item_5)
        bot.send_message(message.chat.id, "Я к Вашим услугам!", reply_markup=markup)
    elif message.text == "Назад":
        hello_message(message)


bot.polling(none_stop=True, interval=0)