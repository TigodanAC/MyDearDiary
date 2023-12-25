import requests
import pandas as pd
from bs4 import BeautifulSoup

id_films = []
names_films = []
types_film = []
rating_films = []
years_films = []
links_films = []

soup = BeautifulSoup(requests.get('https://baskino.org/films/').text, 'lxml')
quotes = soup.find('div', class_='navigation ignore-select').find_all('a')[-2].text
pages_size = int(quotes)
for j in range(0, pages_size):
    print(j)
    url = "https://baskino.org/films/" + "page/" + str(j)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    name_link_year = soup.find_all('div', class_='posttitle') # тут у нас ссылка и название и год
    ratings = soup.find_all('li', class_='current-rating') # тут рейтинг 
    for i in range(0, len(name_link_year)):
        try: 
            name, year = name_link_year[i].text.replace(")", "").replace("\n", "").split("(")
        except ValueError: 
            continue
        rating = ratings[i].text
        link = str(name_link_year[i].find("a")).split(">")[0].split("=")[1][1:-1]
        response1 = requests.get(link)
        soup1 = BeautifulSoup(response1.text, 'lxml')
        soup2 = soup1.find_all("tr")
        flag = 0
        for k in soup2:
            k1 = k.text.replace("\n", "").split(":")
            if k1[0] == "Жанр":
                types_film.append(k1[1])
                flag = 1
                break
        if flag == 0:
            continue
        names_films.append(name)
        rating_films.append(rating)
        years_films.append(year)
        links_films.append(link)

numbers = list(range(1, len(names_films) + 1))
dictionary = {"id_films": numbers, "names_films": names_films, "types_film": types_film, "rating_films": rating_films, "years_films": years_films, "links_films": links_films }
df = pd.DataFrame(dictionary)
df.to_csv('films.csv', index=False)