import pandas as pd
import numpy as np
from datetime import datetime


def calories_norma(sex, age, height, weight):
    if sex == 'f':
        return 655.1 + 9.563 * weight + 1.85 * height - 4.676 * age
    else:
        return 66.5 + 13.75 * weight + 5.003 * height - 6.775 * age


def is_user_exist(user_id):
    csv_data = pd.read_csv("users.csv")
    csv_copy = csv_data.copy()
    for index, row in csv_copy.iterrows():
        if row['user_id'] == user_id:
            return True
    return False


def add_user(user_id, sex, age, height, weight):
    if not is_user_exist(user_id):
        csv_data = pd.read_csv("users.csv")
        calories_count = calories_norma(sex, age, height, weight)
        new_row = {'user_id': user_id, 'sex': sex, 'age': age, 'height': height, 'weight': weight,
                   'calories_norma': calories_count}
        new_data = pd.DataFrame([new_row])
        combined_data = pd.concat([csv_data, new_data], ignore_index=True)
        combined_data.to_csv("users.csv", index=False)


def request(type, argc, argv):
    if type == 'GET':
        if argc == 2 and argv[0] == 'user':
            return is_user_exist(argv[1])
        else:
            print("No such GET request")
    elif type == 'PUT':
        if argc == 6 and argv[0] == 'user':
            add_user(argv[1], argv[2], argv[3], argv[4], argv[5])


