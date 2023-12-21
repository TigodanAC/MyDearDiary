import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import io
from PIL import Image


def dataframe_to_image(dataframe):
    buffer = io.BytesIO()
    dataframe.to_image().save(buffer, format='PNG')
    buffer.seek(0)
    image = Image.open(buffer)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return image_bytes


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
    csv_data = csv_data[csv_data['user_id'] == user_id]
    csv_data.drop('note_text', axis=1, inplace=True)
    return dataframe_to_image(csv_data)


def get_note_by_number(user_id, note_number):
    csv_data = pd.read_csv("notes.csv")
    user_data = {}
    for index, row in csv_data.iterrows():
        if row['user_id'] == str(user_id):
            user_data[row['note_num']] = row['note_text']

    if note_number > len(user_data):
        if len(user_data):
            res = "Записи с таким номером не существует"
        else:
            res = "У Вас нет записей"
    else:
        res = user_data[note_number]

    return res


def clean_all_user_notes(user_id):
    csv_data = pd.read_csv("notes.csv")
    csv_data = csv_data[csv_data['user_id'] != user_id]
    csv_data.to_csv("notes.csv", index=False)


def delete_note_by_number(user_id, note_number):
    ...


def request(type, argc, argv):
    if type == 'GET':
        if argc == 2 and argv[0] == 'user':
            return is_user_exist(argv[1])

        elif argc == 2 and argv[0] == 'note':
            return get_all_user_notes(argv[1])

        elif argc == 3 and argv[0] == 'note':
            return get_note_by_number(argv[1], argv[2])

        else:
            print("No such GET request")

    elif type == 'PUT':
        if argc == 6 and argv[0] == 'user':
            add_user(argv[1], argv[2], argv[3], argv[4], argv[5])

        elif argc == 4 and argv[0] == 'note':
            add_note(argv[1], argv[2], argv[3])

        else:
            print("No such PUT request")

    elif type == 'DELETE':
        if argc == 2 and argv[0] == 'note':
            return clean_all_user_notes(argv[1])

        elif argc == 3 and argv[0] == 'note':
            return delete_note_by_number(argv[1], argv[2])

        else:
            print("No such DELETE request")
