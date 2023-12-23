﻿import telebot
from telebot import types
import re
from data_requests import request

TOKEN = '6662823857:AAERFYvIoJGWreU7_y80R_USjUlWghILRFM'

bot = telebot.TeleBot(TOKEN)
regex_pattern = r'^(m|f)\s+(\d+)\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)$'
last_messages = {}
note_names = {}
list_names = {}


@bot.message_handler(commands=['start'])
def hello_message(message):
    if request('GET', 2, ['user', message.from_user.id]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=3)
        item_1 = types.KeyboardButton(text="Дневник")
        item_2 = types.KeyboardButton(text="Досуг")
        item_3 = types.KeyboardButton(text="Счётчик калорий")
        markup.add(item_1, item_2, item_3)
        bot.send_message(message.chat.id, "И снова здравствуй!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         "Привет, я твой дорогой дневник! С моей помощью ты можешь создавать записи в "
                         "виртуальный дневник, искать книги для досуга, а также считать калории!")
        bot.send_message(message.chat.id,
                         "Для начала, пожалуйста, введите свой пол, возраст, рост и вес в формате: "
                         "'f' или 'm', целое число, число, число\nНапример так: m 27 190.0 81.2")


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "В начало":
        if last_messages.get(message.chat.id):
            del last_messages[message.chat.id]
        if note_names.get(message.chat.id):
            del note_names[message.chat.id]
        if list_names.get(message.chat.id):
            del list_names[message.chat.id]

        hello_message(message)

    elif re.match(regex_pattern, message.text):
        argv = ['user', message.from_user.id]
        argv += message.text.split()
        request("PUT", len(argv), argv)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=3)
        item_1 = types.KeyboardButton(text="Дневник")
        item_2 = types.KeyboardButton(text="Досуг")
        item_3 = types.KeyboardButton(text="Счётчик калорий")
        markup.add(item_1, item_2, item_3)
        bot.send_message(message.chat.id, "Что тебя интересует?", reply_markup=markup)

    elif message.text == "Дневник" or message.text == "К дневнику":
        if last_messages.get(message.chat.id):
            del last_messages[message.chat.id]
        if note_names.get(message.chat.id):
            del note_names[message.chat.id]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
        item_1 = types.KeyboardButton(text="Вывести все записи")
        item_2 = types.KeyboardButton(text="Удалить все записи")
        item_3 = types.KeyboardButton(text="Добавить запись")
        item_4 = types.KeyboardButton(text="Прочесть запись")
        item_5 = types.KeyboardButton(text="Удалить запись")
        item_6 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2, item_3, item_4, item_5, item_6)
        bot.reply_markup = markup
        bot.send_message(message.chat.id, "Что бы ты хотел сделать?", reply_markup=markup)

    elif message.text == "Вывести все записи":
        argv = ['note', message.from_user.id]
        table = request("GET", len(argv), argv)
        bot.send_photo(message.chat.id, photo=table.getvalue())

    elif message.text == "Удалить все записи":
        argv = ['note', message.from_user.id]
        request("DELETE", len(argv), argv)
        bot.send_message(message.chat.id, "Записи успешно удалены!")

    elif message.text == "Добавить запись":
        last_messages[message.chat.id] = 'add'
        bot.send_message(message.chat.id, "Введите название записи")

    elif message.text == "Прочесть запись":
        last_messages[message.chat.id] = 'read'
        bot.send_message(message.chat.id, "Введите номер записи")

    elif message.text == "Удалить запись":
        last_messages[message.chat.id] = 'delete'
        bot.send_message(message.chat.id, "Введите номер записи")

    # elif message.text == "Досуг":
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    #     item_1 = types.KeyboardButton(text="Найти фильм")
    #     item_2 = types.KeyboardButton(text="Найти сериал")
    #     item_3 = types.KeyboardButton(text="Найти книгу")
    #     item_4 = types.KeyboardButton(text="Списки")
    #     item_5 = types.KeyboardButton(text="В начало")
    #     markup.add(item_1, item_2, item_3, item_4, item_5)
    #     bot.send_message(message.chat.id, "Я к Вашим услугам!", reply_markup=markup)
    #
    elif message.text == "Счётчик калорий":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="Списки блюд")
        item_5 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_5)
        bot.send_message(message.chat.id, "Я к Вашим услугам!", reply_markup=markup)

    elif message.text == "Списки блюд" or message.text == "К спискам блюд":
        if last_messages.get(message.chat.id):
            del last_messages[message.chat.id]
        if list_names.get(message.chat.id):
            del list_names[message.chat.id]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=8)
        item_1 = types.KeyboardButton(text="Вывести все списки")
        item_2 = types.KeyboardButton(text="Удалить все списки")
        item_3 = types.KeyboardButton(text="Создать список")
        item_4 = types.KeyboardButton(text="Добавить в список")
        item_5 = types.KeyboardButton(text="Прочесть список")
        item_6 = types.KeyboardButton(text="Удалить из списка")
        item_7 = types.KeyboardButton(text="Удалить список")
        item_8 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8)
        bot.send_message(message.chat.id, "Я к Вашим услугам!", reply_markup=markup)

    elif message.text == "Вывести все списки":
        argv = ['dish_list', message.from_user.id]
        table = request("GET", len(argv), argv)
        bot.send_photo(message.chat.id, photo=table.getvalue())

    elif message.text == "Удалить все списки":
        argv = ['dish_list', message.from_user.id]
        request("DELETE", len(argv), argv)
        bot.send_message(message.chat.id, "Списки успешно удалены!")

    elif message.text == "Создать список":
        last_messages[message.chat.id] = 'create'
        bot.send_message(message.chat.id, "Введите название списка")

    elif message.text == "Добавить в список":
        last_messages[message.chat.id] = 'add_to_list'
        bot.send_message(message.chat.id, "Введите номер списка")

    elif message.text == "Прочесть список":
        last_messages[message.chat.id] = 'read_dishes'
        bot.send_message(message.chat.id, "Введите номер списка")

    elif message.text == "Удалить из списка":
        last_messages[message.chat.id] = 'delete_from_list'
        bot.send_message(message.chat.id, "Введите номер списка")

    elif message.text == "Удалить список":
        last_messages[message.chat.id] = 'delete_list'
        bot.send_message(message.chat.id, "Введите номер списка")

    elif last_messages.get(message.chat.id) == 'add':
        note_names[message.chat.id] = message.text
        last_messages[message.chat.id] = 'text'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item = types.KeyboardButton(text="К дневнику")
        markup.add(item)
        bot.send_message(message.chat.id, "Введите, что хотели бы записать в дневник", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'text':
        del last_messages[message.chat.id]
        name = note_names.pop(message.chat.id)
        argv = ['note', message.from_user.id, name, message.text]
        request("PUT", len(argv), argv)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К дневнику")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)
        bot.send_message(message.chat.id, "Ваша запись успешно добавлена!", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'read':
        markup_good = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_bad = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К дневнику")
        item_2 = types.KeyboardButton(text="В начало")
        item_3 = types.KeyboardButton(text="Вывести все записи")
        markup_good.add(item_1, item_2)
        markup_bad.add(item_3, item_1)

        if message.text.isdigit():
            argv = ['note', message.from_user.id, int(message.text)]
            text = request("GET", len(argv), argv)
            if text:
                del last_messages[message.chat.id]
                bot.send_message(message.chat.id, text, reply_markup=markup_good)
            else:
                bot.send_message(message.chat.id, "Записи с таким номером не существует", reply_markup=markup_bad)
        else:
            bot.send_message(message.chat.id, "Неверный формат номера", reply_markup=markup_bad)

    elif last_messages.get(message.chat.id) == 'delete':
        markup_good = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_bad = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К дневнику")
        item_2 = types.KeyboardButton(text="В начало")
        item_3 = types.KeyboardButton(text="Вывести все записи")
        markup_good.add(item_1, item_2)
        markup_bad.add(item_3, item_1)

        if message.text.isdigit():
            argv = ['note', message.from_user.id, int(message.text)]
            if request("DELETE", len(argv), argv):
                del last_messages[message.chat.id]
                bot.send_message(message.chat.id, "Ваша запись успешно удалена!", reply_markup=markup_good)
            else:
                bot.send_message(message.chat.id, "Записи с таким номером не существует", reply_markup=markup_bad)
        else:
            bot.send_message(message.chat.id, "Неверный формат номера", reply_markup=markup_bad)

    elif last_messages.get(message.chat.id) == 'create':
        list_names[message.chat.id] = message.text
        last_messages[message.chat.id] = 'dishes'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)
        bot.send_message(message.chat.id, "Введите номера блюд, которые хотели бы добавить в список",
                         reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'dishes':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)

        del last_messages[message.chat.id]
        name = list_names.pop(message.chat.id)
        ids = message.text.replace(',', ' ').split()
        for id in ids:
            if not id.isdigit():
                bot.send_message(message.chat.id, "Неверный формат", reply_markup=markup)

        argv = ['dish_list', message.from_user.id, name, ids]
        if request("PUT", len(argv), argv):
            bot.send_message(message.chat.id, "Список успешно создан!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Ошибка при создании списка!", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'add_to_list':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)

        if message.text.isdigit():
            list_names[message.chat.id] = message.text
            last_messages[message.chat.id] = 'list_dish'
            bot.send_message(message.chat.id, "Введите номера блюд, которые хотели бы добавить в список",
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Неверный формат номера", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'list_dish':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)

        del last_messages[message.chat.id]
        name = list_names.pop(message.chat.id)
        ids = message.text.replace(',', ' ').split()
        for id in ids:
            if not id.isdigit():
                bot.send_message(message.chat.id, "Неверный формат", reply_markup=markup)

        argv = ['dish_list_add', message.from_user.id, name, ids]
        if request("PUT", len(argv), argv):
            bot.send_message(message.chat.id, "Блюда успешно добавлены!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Ошибка при добавлении в список!", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'read_dishes':
        markup_good = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_bad = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        item_3 = types.KeyboardButton(text="Вывести все списки")
        markup_good.add(item_1, item_2)
        markup_bad.add(item_3, item_1)

        if message.text.isdigit():
            argv = ['dish_list', message.from_user.id, int(message.text)]
            text = request("GET", len(argv), argv)
            if text:
                del last_messages[message.chat.id]
                bot.send_message(message.chat.id, text, reply_markup=markup_good)
            else:
                bot.send_message(message.chat.id, "Списка с таким номером не существует", reply_markup=markup_bad)
        else:
            bot.send_message(message.chat.id, "Неверный формат номера", reply_markup=markup_bad)

    elif last_messages.get(message.chat.id) == 'delete_from_list':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)

        if message.text.isdigit():
            list_names[message.chat.id] = message.text
            last_messages[message.chat.id] = 'remove_from_list'
            bot.send_message(message.chat.id, "Введите номера блюд, которые хотели бы удалить из списка",
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Неверный формат номера", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'remove_from_list':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        markup.add(item_1, item_2)

        del last_messages[message.chat.id]
        name = list_names.pop(message.chat.id)
        ids = message.text.replace(',', ' ').split()
        for id in ids:
            if not id.isdigit():
                bot.send_message(message.chat.id, "Неверный формат", reply_markup=markup)

        argv = ['dish_list', message.from_user.id, name, ids]
        if request("DELETE", len(argv), argv):
            bot.send_message(message.chat.id, "Блюда успешно удалены", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Ошибка при удалении из списка!", reply_markup=markup)

    elif last_messages.get(message.chat.id) == 'delete_list':
        markup_good = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_bad = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_1 = types.KeyboardButton(text="К спискам блюд")
        item_2 = types.KeyboardButton(text="В начало")
        item_3 = types.KeyboardButton(text="Вывести все списки")
        markup_good.add(item_1, item_2)
        markup_bad.add(item_3, item_1)

        if message.text.isdigit():
            argv = ['dish_list', message.from_user.id, int(message.text)]
            if request("DELETE", len(argv), argv):
                del last_messages[message.chat.id]
                bot.send_message(message.chat.id, "Ваш список успешно удален!", reply_markup=markup_good)
            else:
                bot.send_message(message.chat.id, "Списка с таким номером не существует", reply_markup=markup_bad)
        else:
            bot.send_message(message.chat.id, "Неверный формат номера", reply_markup=markup_bad)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item = types.KeyboardButton(text="В начало")
        markup.add(item)
        bot.send_message(message.chat.id, "Неизвестная комманда, попробуйте снова или вернитесь в начало!",
                         reply_markup=markup)


bot.polling(none_stop=True, interval=0)
