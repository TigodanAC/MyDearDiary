import requests
import pandas as pd
from bs4 import BeautifulSoup

names = []
calories = []
proteins = []
fats = []
carbohydrates = []

urls = {'https://health-diet.ru/base_of_food/food_24507/', 'https://health-diet.ru/base_of_food/food_24523/',
        'https://health-diet.ru/base_of_food/food_24509/', 'https://health-diet.ru/base_of_food/food_24502/',
        'https://health-diet.ru/base_of_food/food_24513/', 'https://health-diet.ru/base_of_food/food_24515/',
        'https://health-diet.ru/base_of_food/food_24525/', 'https://health-diet.ru/base_of_food/food_24522/',
        'https://health-diet.ru/base_of_food/food_24519/', 'https://health-diet.ru/base_of_food/food_24508/',
        'https://health-diet.ru/base_of_food/food_24512/', 'https://health-diet.ru/base_of_food/food_24517/',
        'https://health-diet.ru/base_of_food/food_24506/', 'https://health-diet.ru/base_of_food/food_24501/',
        'https://health-diet.ru/base_of_food/food_24527/', 'https://health-diet.ru/base_of_food/food_24518/',
        'https://health-diet.ru/base_of_food/food_24503/', 'https://health-diet.ru/base_of_food/food_24528/',
        'https://health-diet.ru/base_of_food/food_24511/', 'https://health-diet.ru/base_of_food/food_24504/',
        'https://health-diet.ru/base_of_food/food_24514/', 'https://health-diet.ru/base_of_food/food_24529/',
        'https://health-diet.ru/base_of_food/food_24516/', 'https://health-diet.ru/base_of_food/food_24524/',
        'https://health-diet.ru/base_of_food/food_24524/', 'https://health-diet.ru/base_of_food/food_24520/',
        'https://health-diet.ru/base_of_meals/meals_21252/', 'https://health-diet.ru/base_of_meals/meals_21243/',
        'https://health-diet.ru/base_of_meals/meals_21249/', 'https://health-diet.ru/base_of_meals/meals_21244/',
        'https://health-diet.ru/base_of_meals/meals_21245/', 'https://health-diet.ru/base_of_meals/meals_21254/',
        'https://health-diet.ru/base_of_meals/meals_21250/', 'https://health-diet.ru/base_of_meals/meals_21247/',
        'https://health-diet.ru/base_of_meals/meals_21248/', 'https://health-diet.ru/base_of_meals/meals_21242/',
        'https://health-diet.ru/base_of_meals/meals_21241/', 'https://health-diet.ru/base_of_meals/meals_21251/'}


for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find('tbody').find_all('tr')
    for i in range(0, len(quotes)):
        quotes1 = quotes[i].find('a').text
        names.append(quotes1)
        quotes2 = quotes[i].find_all('td', class_='uk-text-right')
        calories.append(float(quotes2[0].text.replace(",", ".").split()[0]))
        proteins.append(float(quotes2[1].text.replace(",", ".").split()[0]))
        fats.append(float(quotes2[2].text.replace(",", ".").split()[0]))
        carbohydrates.append(float(quotes2[3].text.replace(",", ".").split()[0]))

dictionary = {"Названия": names, "Калорийность": calories, "Белки": proteins, "Жиры": fats, "Углеводы": carbohydrates }

df = pd.DataFrame(dictionary)
df.to_csv('dishes.csv', index=False)