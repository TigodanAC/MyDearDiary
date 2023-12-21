import pandas as pd

names_books = ["Бесы", "Шах и мат"]
types_books = ["Классическая русская литература", "Современные любовные романы"]
authors_books =["Достоевский Федор Михайлович", "Хейзелвуд Али"]
rating_books = [4.7, 4.4]
links_books = ["https://book24.ru/product/besy-5422017/", "https://book24.ru/product/shakh-i-mat-6784435/"]
dictionary1 = {"Название": names_books, "Aвтор": authors_books, "Раздел": types_books, "Рейтинг": rating_books, "Узнать больше": links_books}


names_films = ["Зверополис", "Поезд в Пусан"]
types_films = ["Мультфильм", ["Ужасы", "Боевик"]]
rating_films = [8.3, 7.2]
years_films = ["2016", "2016"]
links_films = ["https://www.kinopoisk.ru/film/775276/", "https://www.kinopoisk.ru/film/977288/"]
dictionary2 = {"Название": names_films, "Жанр": types_films, "Рейтинг": rating_films, "Год выпуска": years_films, "Узнать больше": links_films}

df1 = pd.DataFrame(dictionary1)
df1.to_csv('micro_books.csv', index=False)
df2 = pd.DataFrame(dictionary2)
df2.to_csv('micro_films.csv', index=False)