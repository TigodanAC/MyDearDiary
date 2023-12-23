import ast
from io import BytesIO
from random import random
import random
import pandas as pd
import numpy as np
from datetime import datetime
import dataframe_image as dfi


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
            if row['names_books'] == str(book):
                books_dict[row['authors_books']] = str(book)
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


def add_film_list(user_id, list_title, film_names):
    csv_data = pd.read_csv("wishlist_films.csv")
    csv_copy = csv_data.copy()
    list_num = 1
    for index, row in csv_copy.iterrows():
        if row['user_id'] == str(user_id):
            list_num += 1
    films_dict = {}
    csv_films = pd.read_csv("micro_films.csv")
    for film in film_names:
        for index, row in csv_films.iterrows():
            if row['names_films'] == str(film):
                films_dict[row['years_films']] = str(film)
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


# Непонятно, что делать в случае нескольких списков с одним названием"
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


# Непонятно, что делать в случае нескольких списков с одним названием
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


# Непонятно, что делать в случае нескольких списков с одним названием"
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


# Непонятно, что делать в случае нескольких списков с одним названием"
def get_dish_list_by_title(user_id, list_title):
    csv_data = pd.read_csv("wishlist_dishes.csv")
    dishes_list = []
    for index, row in csv_data.iterrows():
        if row['user_id'] == user_id and str(row['list_dish_title']) == str(list_title):
            dishes_dict = ast.literal_eval(row['list_dish_names'])
            dishes_list = [dishes_dict[key] for key in dishes_dict]
            break
    return ', '.join(dishes_list)


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


def add_dish_to_eaten(user_id, dish_number):
    csv_calories = pd.read_csv("calories.csv")
    csv_dishes = pd.read_csv("dishes.csv")
    flag = False
    for index, row in csv_dishes.iterrows():
        if str(row['id_meals']) == str(dish_number):
            flag = True
            add_user_dish(user_id, row['calories'], row['proteins'], row['fats'], row['carbohydrates'])
    return flag


def add_dish_list_to_eaten(user_id, dish_list):
    csv_data = pd.read_csv("calories.csv")
    csv_dishes = pd.read_csv("dishes.csv")
    flag = False
    for dish in dish_list:
        for index, row in csv_dishes.iterrows():
            if str(row['id_meals']) == str(dish):
                flag = True
                add_user_dish(user_id, row['calories'], row['proteins'], row['fats'], row['carbohydrates'])
    return flag


def get_random_dishes():
    csv_dishes = pd.read_csv("dishes.csv")
    random_rows = random.sample(range(len(csv_dishes)), 30)
    need_df = csv_dishes.iloc[random_rows]
    print(need_df)
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
    dishes_list = pd.DataFrame(columns=['id_meals', 'meals_names', 'calories', 'proteins', 'fats', 'carbohydrates'])
    for index, row in csv_data.iterrows():
        counter = 0
        for word in word_list:
            if word in row['meals_names']:
                counter += 1
        if counter == len(word_list):
            for word in word_list:
                new_data = pd.DataFrame([row])
                if dishes_list.empty:
                    dishes_list = new_data
                else:
                    dishes_list = pd.concat([dishes_list, new_data], ignore_index=True)
    dishes_list = dishes_list.drop_duplicates()
    if len(dishes_list) > 50:
        dishes_list = dishes_list.head(50)
    print(dishes_list)
    new_column_names = {'id_meals': 'Номер', 'meals_names': 'Название блюда', 'calories': 'Число калорий',
                        'proteins': 'Число белков', 'fats': 'Число жиров', 'carbohydrates': 'Число углеводов'}
    df = dishes_list.rename(columns=new_column_names).reset_index(drop=True)
    df_styled = df.style.set_properties(**{'text-align': 'center'}).hide()
    buf = BytesIO()
    dfi.export(df_styled, buf)
    return buf


def request(type, argc, argv):
    if type == 'GET':
        if argc == 2 and argv[0] == 'user':
            return is_user_exist(argv[1])

        elif argc == 2 and argv[0] == 'note':
            return get_all_user_notes(argv[1])

        elif argc == 3 and argv[0] == 'note':
            return get_note_by_number(argv[1], argv[2])

        elif argc == 2 and argv[0] == 'dish_list':
            return get_all_user_dish_lists(argv[1])

        elif argc == 3 and argv[0] == 'dish_list':
            return get_dish_list_by_number(argv[1], argv[2])

        elif argc == 3 and argv[0] == 'dish_list_t':
            return get_dish_list_by_title(argv[1], argv[2])

        elif argc == 1 and argv[0] == 'dishes':
            return get_random_dishes()

        elif argc == 2 and argv[0] == 'dishes':
            return get_certain_dishes_by_words(argv[1])

        else:
            print("No such GET request")

    elif type == 'PUT':
        if argc == 6 and argv[0] == 'user':
            add_user(argv[1], argv[2], argv[3], argv[4], argv[5])

        elif argc == 4 and argv[0] == 'note':
            add_note(argv[1], argv[2], argv[3])

        elif argc == 4 and argv[0] == 'dish_list':
            return add_dish_list(argv[1], argv[2], argv[3])

        elif argc == 4 and argv[0] == 'book_list':
            return add_book_list(argv[1], argv[2], argv[3])

        elif argc == 4 and argv[0] == 'film_list':
            return add_film_list(argv[1], argv[2], argv[3])

        elif argc == 4 and argv[0] == 'dish_list_add':
            return add_in_dish_list_by_number(argv[1], argv[2], argv[3])

        elif argc == 4 and argv[0] == 'dish_list_t':
            return add_in_dish_list_by_title(argv[1], argv[2], argv[3])

        elif argc == 3 and argv[0] == 'calories':
            return add_dish_to_eaten(argv[1], argv[2])

        elif argc == 3 and argv[0] == 'calories_list':
            return add_dish_list_to_eaten(argv[1], argv[2])

        else:
            print("No such PUT request")

    elif type == 'DELETE':
        if argc == 2 and argv[0] == 'note':
            clean_all_user_notes(argv[1])

        elif argc == 3 and argv[0] == 'note':
            return delete_note_by_number(argv[1], argv[2])

        elif argc == 2 and argv[0] == 'dish_list':
            clean_all_user_dish_lists(argv[1])

        elif argc == 3 and argv[0] == 'dish_list':
            return delete_dish_list_by_number(argv[1], argv[2])

        elif argc == 3 and argv[0] == 'dish_list_t':
            return delete_dish_list_by_title(argv[1], argv[2])

        elif argc == 4 and argv[0] == 'dish_list':
            return delete_in_dish_list_by_number(argv[1], argv[2], argv[3])

        elif argc == 4 and argv[0] == 'dish_list_t':
            return delete_in_dish_list_by_title(argv[1], argv[2], argv[3])

        else:
            print("No such DELETE request")
