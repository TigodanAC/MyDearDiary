import ast
import io
import json
from collections import deque
from io import BytesIO
from random import random
import random
import pandas as pd
import numpy as np
from datetime import datetime
import dataframe_image as dfi
from matplotlib import pyplot as plt
import threading


def calories_norma(sex, age, height, weight):
    if sex == 'f':
        return 655.1 + 9.563 * weight + 1.85 * height - 4.676 * age
    else:
        return 66.5 + 13.75 * weight + 5.003 * height - 6.775 * age


def is_user_exist(user_id):
    csv_data = pd.read_csv("users.csv")
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id):
            return True
    return False


def add_user(user_id, sex, age, height, weight):
    if not is_user_exist(user_id):
        csv_data = pd.read_csv("users.csv")
        age = int(age)
        height = float(height)
        weight = float(weight)
        calories_count = calories_norma(sex, age, height, weight)
        new_row = {'user_id': user_id, 'sex': sex, 'age': age, 'height': height, 'weight': weight,
                   'calories_norma': calories_count}
        new_data = pd.DataFrame([new_row])
        combined_data = pd.concat([csv_data, new_data], ignore_index=True)
        combined_data.to_csv("users.csv", index=False)


def add_note(user_id, note_name, note_text):
    csv_data = pd.read_csv("notes.csv")
    csv_copy = csv_data.copy()
    note_num = 1
    for index, row in csv_copy.iterrows():
        if row['user_id'] == str(user_id):
            note_num += 1
    current_datetime = datetime.now().strftime('%d.%m.%Y %H.%M.%S')
    new_row = {'user_id': user_id, 'note_num': note_num, 'note_date': current_datetime, 'note_name': note_name,
               'note_text': note_text}
    new_data = pd.DataFrame([new_row])
    combined_data = pd.concat([csv_data, new_data], ignore_index=True)
    combined_data.to_csv("notes.csv", index=False)


def get_all_user_notes(user_id):
    csv_data = pd.read_csv("notes.csv")
    csv_data = csv_data[csv_data['user_id'] == str(user_id)]
    csv_data.drop('note_text', axis=1, inplace=True)
    csv_data.drop('user_id', axis=1, inplace=True)
    new_column_names = {'note_num': 'Номер', 'note_date': 'Дата создания', 'note_name': 'Название записи'}
    df = csv_data.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def get_note_by_number(user_id, note_number):
    csv_data = pd.read_csv("notes.csv")
    user_data = {}
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id):
            user_data[row['note_num']] = row['note_text']

    if note_number > len(user_data):
        res = ''
    else:
        res = user_data[note_number]

    return res


def clean_all_user_notes(user_id):
    csv_data = pd.read_csv("notes.csv")
    csv_data = csv_data[csv_data['user_id'] != str(user_id)]
    csv_data.to_csv("notes.csv", index=False)


def delete_note_by_number(user_id, note_number):
    csv_data = pd.read_csv("notes.csv")
    csv_copy = csv_data[(csv_data['user_id'] == str(user_id)) & (csv_data['note_num'] == note_number)]
    if len(csv_copy):
        csv_data = csv_data.drop(csv_copy.index)
        csv_data.loc[
            (csv_data['user_id'] == str(user_id)) & (csv_data['note_num'] > note_number), 'note_num'] -= 1
        csv_data.to_csv("notes.csv", index=False)
        return True
    return False


def add_dish_list(user_id, list_title, dish_numbers):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    csv_copy = csv_data.copy()
    list_num = 1
    for index, row in csv_copy.iterrows():
        if row['user_id'] == str(user_id):
            list_num += 1
    dishes_dict = {}
    csv_dishes = pd.read_csv("dishes.csv")
    for num in dish_numbers:
        for index, row in csv_dishes.iterrows():
            if str(row['id_meals']) == str(num):
                dishes_dict[row['id_meals']] = row['meals_names']
                break
    if len(dishes_dict):
        new_row = {'user_id': user_id, 'list_dish_number': str(list_num), 'list_dish_title': list_title,
                   'list_dish_names': dishes_dict}
        new_data = pd.DataFrame([new_row])
        combined_data = pd.concat([csv_data, new_data], ignore_index=True)
        combined_data[['user_id', 'list_dish_number', 'list_dish_title', 'list_dish_names']].to_csv(
            "wishlist_dishes.csv", index=False)
        return True
    return False


def add_in_dish_list_by_number(user_id, list_number, dish_numbers):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    csv_dishes = pd.read_csv("dishes.csv")
    flag = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and str(row['list_dish_number']) == str(list_number):
            flag = True
            dishes_dict = eval(row['list_dish_names'])
            for num in dish_numbers:
                for idx, r in csv_dishes.iterrows():
                    if str(r['id_meals']) == str(num):
                        dishes_dict[r['id_meals']] = r['meals_names']
                        break
            csv_data.at[index, 'list_dish_names'] = str(dishes_dict)
    csv_data.to_csv("wishlist_dishes.csv", index=False)
    return flag


def add_in_dish_list_by_title(user_id, list_title, dish_numbers):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    csv_dishes = pd.read_csv("dishes.csv")
    flag = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and row['list_dish_title'] == str(list_title):
            flag = True
            dishes_dict = eval(row['list_dish_names'])
            for num in dish_numbers:
                for idx, r in csv_dishes.iterrows():
                    if str(r['id_meals']) == str(num):
                        dishes_dict[r['id_meals']] = r['meals_names']
                        break
            csv_data.at[index, 'list_dish_names'] = str(dishes_dict)
    csv_data.to_csv("wishlist_dishes.csv", index=False)
    return flag


def delete_dish_list_by_number(user_id, list_number):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    deleted = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and int(row['list_dish_number']) == list_number:
            csv_data = csv_data.drop(index)
            deleted = True
        elif deleted and row['user_id'] == str(user_id):
            csv_data.at[index, 'list_dish_number'] = int(row['list_dish_number']) - 1
    if deleted:
        csv_data.to_csv("wishlist_dishes.csv", index=False)
        return True
    return False


def delete_dish_list_by_title(user_id, list_title):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    list_num_to_update = None
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and row['list_dish_title'] == str(list_title):
            list_num_to_update = int(row['list_dish_number'])
            csv_data = csv_data.drop(index)
    if list_num_to_update is not None:
        for index, row in csv_data.iterrows():
            if row['user_id'] == str(user_id) and int(row['list_dish_number']) > list_num_to_update:
                csv_data.at[index, 'list_dish_number'] = int(row['list_dish_number']) - 1
        csv_data.to_csv("wishlist_dishes.csv", index=False)
        return True
    return False


def delete_in_dish_list_by_number(user_id, list_number, dish_numbers):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    flag = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and str(row['list_dish_number']) == str(list_number):
            flag = True
            dishes_dict = eval(row['list_dish_names'])
            for num in dish_numbers:
                for key, value in list(dishes_dict.items()):
                    if str(key) == str(num):
                        del dishes_dict[key]
            csv_data.at[index, 'list_dish_names'] = str(dishes_dict)
    csv_data.to_csv("wishlist_dishes.csv", index=False)
    return flag


def delete_in_dish_list_by_title(user_id, list_title, dish_numbers):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    flag = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and row['list_dish_title'] == str(list_title):
            flag = True
            dishes_dict = eval(row['list_dish_names'])
            for num in dish_numbers:
                for key, value in list(dishes_dict.items()):
                    if str(key) == str(num):
                        del dishes_dict[key]
            csv_data.at[index, 'list_dish_names'] = str(dishes_dict)
    csv_data.to_csv("wishlist_dishes.csv", index=False)
    return flag


def clean_all_user_dish_lists(user_id):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    csv_data = csv_data[csv_data['user_id'] != str(user_id)]
    csv_data.to_csv("wishlist_dishes.csv", index=False)


def get_all_user_dish_lists(user_id):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    csv_data = csv_data[csv_data['user_id'] == str(user_id)]
    csv_data.drop('list_dish_names', axis=1, inplace=True)
    csv_data.drop('user_id', axis=1, inplace=True)
    new_column_names = {'list_dish_number': 'Номер', 'list_dish_title': 'Название списка'}
    df = csv_data.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def get_dish_list_by_number(user_id, list_number):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    dishes_list = []
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and int(row['list_dish_number']) == list_number:
            dishes_dict = ast.literal_eval(row['list_dish_names'])
            dishes_list = [dishes_dict[key] for key in dishes_dict]
            if dishes_list:
                return '\n'.join(dishes_list)
            else:
                return 'Список пуст('
    return False


def get_dish_list_by_title(user_id, list_title):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    dishes_list = []
    for index, row in csv_data.iterrows():
        if row['user_id'] == user_id and str(row['list_dish_title']) == str(list_title):
            dishes_dict = ast.literal_eval(row['list_dish_names'])
            dishes_list = [dishes_dict[key] for key in dishes_dict]
            break
    return ', '.join(dishes_list)


def get_dish_info(dish_number):
    csv_data = pd.read_csv("dishes.csv")
    for index, row in csv_data.iterrows():
        if str(row['id_meals']) == str(dish_number):
            name = 'Название: ' + str(row['meals_names'])
            calories = 'Калорийность: ' + str(row['calories'])
            proteins = 'Белки: ' + str(row['proteins'])
            fats = 'Жиры: ' + str(row['fats'])
            carbohydrates = 'Углеводы: ' + str(row['carbohydrates'])
            info = [name, calories, proteins, fats, carbohydrates]
            return '\n'.join(info)


def get_random_dishes():
    csv_dishes = pd.read_csv("dishes.csv")
    random_rows = random.sample(range(len(csv_dishes)), 10)
    need_df = csv_dishes.iloc[random_rows]
    new_column_names = {'id_meals': 'Номер', 'meals_names': 'Название блюда', 'calories': 'Число калорий',
                        'proteins': 'Число белков', 'fats': 'Число жиров', 'carbohydrates': 'Число углеводов'}
    df = need_df.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def get_certain_dishes_by_words(words):
    csv_data = pd.read_csv("dishes.csv")
    words = words.replace(",", " ")
    word_list = words.split()
    word_list = [word.lower() for word in word_list]
    dishes_list = pd.DataFrame(columns=['id_meals', 'meals_names', 'calories', 'proteins', 'fats', 'carbohydrates'])
    for index, row in csv_data.iterrows():
        counter = 0
        for word in word_list:
            if word in row['meals_names'].lower():
                counter += 1
        if counter == len(word_list):
            new_data = pd.DataFrame([row])
            if dishes_list.empty:
                dishes_list = new_data
            else:
                dishes_list = pd.concat([dishes_list, new_data], ignore_index=True)
    if len(dishes_list) > 10:
        random_rows = random.sample(range(len(dishes_list)), 10)
        dishes_list = dishes_list.iloc[random_rows]
    elif dishes_list.empty:
        return False
    new_column_names = {'id_meals': 'Номер', 'meals_names': 'Название блюда', 'calories': 'Число калорий',
                        'proteins': 'Число белков', 'fats': 'Число жиров', 'carbohydrates': 'Число углеводов'}
    df = dishes_list.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def add_user_dish(user_id, a, b, c, d):
    csv_calories = pd.read_csv("calories.csv")
    user_row = csv_calories[csv_calories['user_id'] == str(user_id)]
    if not user_row.empty:
        user_index = user_row.index[0]
        csv_calories.at[user_index, 'today_count_calories'] = float(
            user_row['today_count_calories'].iloc[0]) + a
        csv_calories.at[user_index, 'today_count_proteins'] = float(
            user_row['today_count_proteins'].iloc[0]) + b
        csv_calories.at[user_index, 'today_count_fats'] = float(user_row['today_count_fats'].iloc[0]) + c
        csv_calories.at[user_index, 'today_count_carbohydrates'] = float(
            user_row['today_count_carbohydrates'].iloc[0]) + d
    else:
        new_row = {'user_id': user_id, 'today_count_calories': a,
                   'today_count_proteins': b,
                   'today_count_fats': c,
                   'today_count_carbohydrates': d,
                   'recent_week_info': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                                        [0, 0, 0, 0], [0, 0, 0, 0]]}
        new_data = pd.DataFrame([new_row])
        if not csv_calories.empty:
            csv_calories = pd.concat([csv_calories, new_data], ignore_index=True, join='inner')
        else:
            csv_calories = new_data
    csv_calories = csv_calories.round(2)
    csv_calories[
        ['user_id', 'today_count_calories', 'today_count_proteins', 'today_count_fats', 'today_count_carbohydrates',
         'recent_week_info']].to_csv(
        "calories.csv", index=False)


def add_dishes_to_eaten(user_id, dishes):
    csv_dishes = pd.read_csv("dishes.csv")
    flag = False
    for dish in dishes:
        for index, row in csv_dishes.iterrows():
            if str(row['id_meals']) == str(dish):
                flag = True
                add_user_dish(user_id, row['calories'], row['proteins'], row['fats'], row['carbohydrates'])
    return flag


def add_dish_list_to_eaten(user_id, dish_list_number):
    csv_dishes = pd.read_csv("wishlist_dishes.csv")
    csv_lists = csv_dishes[csv_dishes['user_id'] == str(user_id)]
    flag = False
    for index, row in csv_lists.iterrows():
        if str(row['list_dish_number']) == str(dish_list_number):
            flag = True
            for key in eval(row['list_dish_names']):
                add_dishes_to_eaten(user_id, [key])
    return flag


def finish_day(user_id):
    csv_calories = pd.read_csv("calories.csv")
    csv_users = pd.read_csv("users.csv")
    user_row_one = csv_users[csv_users['user_id'] == str(user_id)]
    if is_user_exist(user_id):
        user_row_one = csv_users[csv_users['user_id'] == str(user_id)].iloc[0]
    user_row = csv_calories[csv_calories['user_id'] == str(user_id)]
    if not user_row.empty:
        user_index = user_row.index[0]
        remember = user_row['today_count_calories']
        today_info = [round(float(user_row[col].iloc[0]), 2) for col in
                      ['today_count_calories', 'today_count_proteins', 'today_count_fats', 'today_count_carbohydrates']]

        csv_calories.at[user_index, 'today_count_calories'] = 0
        csv_calories.at[user_index, 'today_count_proteins'] = 0
        csv_calories.at[user_index, 'today_count_fats'] = 0
        csv_calories.at[user_index, 'today_count_carbohydrates'] = 0
        line = json.loads(user_row['recent_week_info'].iloc[0])
        output_list = [[round(float(num), 2) for num in sublist] for sublist in line]
        day_queue = deque(output_list)
        day_queue.popleft()
        day_queue.append(today_info)
        csv_calories.at[user_index, 'recent_week_info'] = str(list(day_queue))
        if is_user_exist(user_id):
            res = 'Сегодня ты потребил ' + str(remember.iloc[0]) + ' ккал при суточной норме ' + str(
                user_row_one['calories_norma']) + ' ккал'
        else:
            res = 'Сегодня ты потребил ' + str(remember.iloc[
                                                   0]) + ' ккал. Добавься в качетсве пользователя, чтобы я рассчитал твою суточную норму калорий. Тогда ты сможешь увидеть отклонение от суточной нормы!'
    else:
        res = 'Добавь что-нибудь в "Съеденное" впервые, чтобы начать вести учёт калорий по дням!'
    csv_calories[
        ['user_id', 'today_count_calories', 'today_count_proteins', 'today_count_fats', 'today_count_carbohydrates',
         'recent_week_info']].to_csv("calories.csv", index=False)
    return res


def show_recent_week_statistic(user_id):
    csv_calories = pd.read_csv("calories.csv")
    csv_users = pd.read_csv("users.csv")
    user_row = csv_calories[csv_calories['user_id'] == str(user_id)]
    if not user_row.empty:
        line = json.loads(user_row['recent_week_info'].iloc[0])
        output_list = [[round(float(num), 2) for num in sublist] for sublist in line]
        transformed_list = [[lst[i] for lst in output_list] for i in range(4)]
        plt.figure(figsize=(12, 7))
        plt.plot(range(1, 8), transformed_list[0], label='Калории')
        plt.plot(range(1, 8), transformed_list[1], 'g', label='Белки')
        plt.plot(range(1, 8), transformed_list[2], 'r', label='Жиры')
        plt.plot(range(1, 8), transformed_list[3], 'orange', label='Углеводы')
        if is_user_exist(user_id):
            user_row_one = csv_users[csv_users['user_id'] == str(user_id)].iloc[0]
            plt.axhline(y=float(user_row_one['calories_norma']), color='c', linestyle='--',
                        label='Суточная норма калорий')
        plt.xlabel('Дни', fontweight='bold', fontsize=11)
        plt.ylabel('Количество', fontweight='bold', fontsize=11)
        plt.title('Питание за последнюю неделю', fontweight='bold', fontsize=15)
        plt.xticks(range(1, 8),
                   ['7 дней назад', '6 дней назад', '5 дней назад', '4 дня назад', '3 дня назад', '2 дня назад',
                    '1 день назад'], fontstyle='italic', rotation=15)
        plt.legend(loc='upper right')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        return buffer
    else:
        return False


def add_film_list(user_id, list_title, film_names):
    csv_data = pd.read_csv("wishlist_films.csv")
    csv_copy = csv_data.copy()
    csv_films = pd.read_csv("films.csv")
    list_num = 1
    for index, row in csv_copy.iterrows():
        if row['user_id'] == str(user_id):
            list_num += 1
    films_dict = {}
    for film in film_names:
        for index, row in csv_films.iterrows():
            if str(row['id_films']) == str(film):
                films_dict[row['id_films']] = row['names_films']
                break
    if len(films_dict):
        new_row = {'user_id': user_id, 'list_film_number': str(list_num), 'list_film_title': list_title,
                   'list_film_names': films_dict}
        new_data = pd.DataFrame([new_row])
        combined_data = pd.concat([csv_data, new_data], ignore_index=True)
        combined_data[['user_id', 'list_film_number', 'list_film_title', 'list_film_names']].to_csv(
            "wishlist_films.csv", index=False)
        return True
    return False


def add_in_film_list_by_number(user_id, list_number, film_numbers):
    csv_data = pd.read_csv("wishlist_films.csv")
    csv_films = pd.read_csv("films.csv")
    flag = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and str(row['list_film_number']) == str(list_number):
            flag = True
            films_dict = eval(row['list_film_names'])
            for num in film_numbers:
                for idx, r in csv_films.iterrows():
                    if str(r['id_films']) == str(num):
                        films_dict[r['id_films']] = r['names_films']
                        break
            csv_data.at[index, 'list_film_names'] = str(films_dict)
    csv_data.to_csv("wishlist_films.csv", index=False)
    return flag


def delete_film_list_by_number(user_id, list_number):
    csv_data = pd.read_csv("wishlist_films.csv")
    deleted = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and int(row['list_film_number']) == list_number:
            csv_data = csv_data.drop(index)
            deleted = True
        elif deleted and row['user_id'] == str(user_id):
            csv_data.at[index, 'list_film_number'] = int(row['list_film_number']) - 1
    if deleted:
        csv_data.to_csv("wishlist_films.csv", index=False)
        return True
    return False


def delete_in_film_list_by_number(user_id, list_number, film_numbers):
    csv_data = pd.read_csv("wishlist_films.csv")
    flag = False
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and str(row['list_film_number']) == str(list_number):
            flag = True
            films_dict = eval(row['list_film_names'])
            for num in film_numbers:
                for key, value in list(films_dict.items()):
                    if str(key) == str(num):
                        del films_dict[key]
            csv_data.at[index, 'list_film_names'] = str(films_dict)
    csv_data.to_csv("wishlist_films.csv", index=False)
    return flag


def clean_all_user_film_lists(user_id):
    csv_data = pd.read_csv("wishlist_films.csv")
    csv_data = csv_data[csv_data['user_id'] != str(user_id)]
    csv_data.to_csv("wishlist_films.csv", index=False)


def get_all_user_film_lists(user_id):
    csv_data = pd.read_csv("wishlist_films.csv")
    csv_data = csv_data[csv_data['user_id'] == str(user_id)]
    csv_data.drop('list_film_names', axis=1, inplace=True)
    csv_data.drop('user_id', axis=1, inplace=True)
    new_column_names = {'list_film_number': 'Номер', 'list_film_title': 'Название списка'}
    df = csv_data.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def get_film_list_by_number(user_id, list_number):
    csv_data = pd.read_csv("wishlist_films.csv")
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id) and int(row['list_film_number']) == list_number:
            films_dict = ast.literal_eval(row['list_film_names'])
            films_list = [films_dict[key] for key in films_dict]
            if films_list:

                return '\n'.join(films_list)
            else:
                return 'Список пуст('
    return False


def get_certain_films_by_words(words):
    csv_data = pd.read_csv("films.csv")
    words = words.replace(",", " ")
    word_list = words.split()
    word_list = [word.lower() for word in word_list]
    film_list = pd.DataFrame(columns=['names_films', 'types_film', 'rating_films', 'years_films'])
    for index, row in csv_data.iterrows():
        counter = 0
        for word in word_list:
            if word in row['names_films'].lower():
                counter += 1
        if counter == len(word_list):
            new_data = pd.DataFrame([row])
            new_data.drop('links_films', axis=1, inplace=True)
            if film_list.empty:
                film_list = new_data
            else:
                film_list = pd.concat([film_list, new_data], ignore_index=True)
    if len(film_list) > 10:
        random_rows = random.sample(range(len(film_list)), 10)
        film_list = film_list.iloc[random_rows]
    elif film_list.empty:
        return False
    new_column_names = {'id_films': 'Номер', 'names_films': 'Название', 'types_film': 'Жанры',
                        'rating_films': 'Рейтинг', 'years_films': 'Год выпуска'}
    df = film_list.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def find_films_by_tags(tags):
    csv_data = pd.read_csv("films.csv")
    tags = tags.replace(",", " ")
    word_list = tags.split()
    word_list = [word.lower() for word in word_list]
    film_list = pd.DataFrame(columns=['names_films', 'types_film', 'rating_films', 'years_films'])
    for index, row in csv_data.iterrows():
        new_row = row['types_film'].lower().replace(",", " ")
        new_row = new_row.split()
        counter = 0
        for tag in word_list:
            for word in new_row:
                if tag == word:
                    counter += 1
        if counter == len(word_list):
            new_data = pd.DataFrame([row])
            new_data.drop('links_films', axis=1, inplace=True)
            if film_list.empty:
                film_list = new_data
            else:
                film_list = pd.concat([film_list, new_data], ignore_index=True)
    if len(film_list) > 10:
        random_rows = random.sample(range(len(film_list)), 10)
        film_list = film_list.iloc[random_rows]
    elif film_list.empty:
        return False
    new_column_names = {'id_films': 'Номер', 'names_films': 'Название', 'types_film': 'Жанры',
                        'rating_films': 'Рейтинг', 'years_films': 'Год выпуска'}
    df = film_list.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def get_random_films():
    csv_data = pd.read_csv("films.csv")
    random_rows = random.sample(range(len(csv_data)), 10)
    need_df = csv_data.iloc[random_rows]
    need_df.drop('links_films', axis=1, inplace=True)
    new_column_names = {'id_films': 'Номер', 'names_films': 'Название', 'types_film': 'Жанры',
                        'rating_films': 'Рейтинг', 'years_films': 'Год выпуска'}
    df = need_df.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def get_film_info(film_number):
    csv_data = pd.read_csv("films.csv")
    for index, row in csv_data.iterrows():
        if str(row['id_films']) == str(film_number):
            name = 'Название: ' + str(row['names_films'])
            types = 'Жанры: ' + str(row['types_film'])
            rating = 'Рейтинг: ' + str(row['rating_films'])
            year = 'Год выпуска: ' + str(row['years_films'])
            link = 'Узнать больше: ' + str(row['links_films'])
            info = [name, types, rating, year, link]
            return '\n'.join(info)


def add_book_list(user_id, list_title, book_names):
    csv_data = pd.read_csv("wishlist_books.csv")
    csv_copy = csv_data.copy()
    list_num = 1
    for index, row in csv_copy.iterrows():
        if row['user_id'] == str(user_id):
            list_num += 1
    books_dict = {}
    csv_books = pd.read_csv("micro_books.csv")
    for book in book_names:
        for index, row in csv_books.iterrows():
            if row['id_books'] == str(book):
                books_dict[row['id_books']] = row['names_books']
                break
    if len(books_dict):
        new_row = {'user_id': user_id, 'list_book_number': str(list_num), 'list_book_title': list_title,
                   'list_book_names': books_dict}
        new_data = pd.DataFrame([new_row])
        combined_data = pd.concat([csv_data, new_data], ignore_index=True)
        combined_data[['user_id', 'list_book_number', 'list_book_title', 'list_book_names']].to_csv(
            "wishlist_books.csv", index=False)
        return True
    return False


def request(type, argc, argv, lock):
    result = False
    if type == 'GET':
        if argc == 2 and argv[0] == 'user':
            result = is_user_exist(argv[1])
        elif argc == 2 and argv[0] == 'note':
            result = get_all_user_notes(argv[1])
        elif argc == 3 and argv[0] == 'note':
            result = get_note_by_number(argv[1], argv[2])
        elif argc == 2 and argv[0] == 'dish_list':
            result = get_all_user_dish_lists(argv[1])
        elif argc == 2 and argv[0] == 'film_list':
            result = get_all_user_film_lists(argv[1])
        elif argc == 3 and argv[0] == 'dish_list':
            result = get_dish_list_by_number(argv[1], argv[2])
        elif argc == 3 and argv[0] == 'film_list':
            result = get_film_list_by_number(argv[1], argv[2])
        elif argc == 3 and argv[0] == 'dish_list_t':
            result = get_dish_list_by_title(argv[1], argv[2])
        elif argc == 1 and argv[0] == 'dishes':
            result = get_random_dishes()
        elif argc == 1 and argv[0] == 'films':
            result = get_random_films()
        elif argc == 2 and argv[0] == 'dishes':
            result = get_certain_dishes_by_words(argv[1])
        elif argc == 2 and argv[0] == 'film_by_words':
            result = get_certain_films_by_words(argv[1])
        elif argc == 2 and argv[0] == 'film_by_tags':
            result = find_films_by_tags(argv[1])
        elif argc == 2 and argv[0] == 'dish':
            result = get_dish_info(argv[1])
        elif argc == 2 and argv[0] == 'film':
            result = get_film_info(argv[1])
        elif argc == 2 and argv[0] == 'plot':
            result = show_recent_week_statistic(argv[1])
        else:
            print("No such GET request")
    elif type == 'PUT':
        lock.acquire()
        if argc == 6 and argv[0] == 'user':
            add_user(argv[1], argv[2], argv[3], argv[4], argv[5])
        elif argc == 4 and argv[0] == 'note':
            add_note(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'dish_list':
            result = add_dish_list(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'book_list':
            result = add_book_list(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'film_list':
            result = add_film_list(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'dish_list_add':
            result = add_in_dish_list_by_number(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'film_list_add':
            result = add_in_film_list_by_number(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'dish_list_t':
            result = add_in_dish_list_by_title(argv[1], argv[2], argv[3])
        elif argc == 3 and argv[0] == 'calories':
            result = add_dishes_to_eaten(argv[1], argv[2])
        elif argc == 3 and argv[0] == 'calories_list':
            result = add_dish_list_to_eaten(argv[1], argv[2])
        elif argc == 2 and argv[0] == 'calories':
            result = finish_day(argv[1])
        else:
            print("No such PUT request")
        lock.release()
    elif type == 'DELETE':
        lock.acquire()
        if argc == 2 and argv[0] == 'note':
            clean_all_user_notes(argv[1])
        elif argc == 3 and argv[0] == 'note':
            result = delete_note_by_number(argv[1], argv[2])
        elif argc == 2 and argv[0] == 'dish_list':
            clean_all_user_dish_lists(argv[1])
        elif argc == 2 and argv[0] == 'film_list':
            clean_all_user_film_lists(argv[1])
        elif argc == 3 and argv[0] == 'dish_list':
            result = delete_dish_list_by_number(argv[1], argv[2])
        elif argc == 3 and argv[0] == 'film_list':
            result = delete_film_list_by_number(argv[1], argv[2])
        elif argc == 3 and argv[0] == 'dish_list_t':
            result = delete_dish_list_by_title(argv[1], argv[2])
        elif argc == 4 and argv[0] == 'dish_list':
            result = delete_in_dish_list_by_number(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'film_list':
            result = delete_in_film_list_by_number(argv[1], argv[2], argv[3])
        elif argc == 4 and argv[0] == 'dish_list_t':
            result = delete_in_dish_list_by_title(argv[1], argv[2], argv[3])
        else:
            print("No such DELETE request")
        lock.release()
    else:
        print("No such request's type")
    return result
