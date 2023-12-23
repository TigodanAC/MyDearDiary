import pandas as pd

names_books = ["Бесы", "Шах и мат"]
types_books = ["Классическая русская литература", "Современные любовные романы"]
authors_books =["Достоевский Федор Михайлович", "Хейзелвуд Али"]
rating_books = [4.7, 4.4]
links_books = ["https://book24.ru/product/besy-5422017/", "https://book24.ru/product/shakh-i-mat-6784435/"]
dictionary1 = {"names_books": names_books, "authors_books": authors_books, "types_books": types_books, "rating_books": rating_books, "links_books": links_books}


names_films = ["Зверополис", "Поезд в Пусан"]
types_films = ["Мультфильм", "Ужасы, Боевик"]
rating_films = [8.3, 7.2]
years_films = ["2016", "2016"]
links_films = ["https://www.kinopoisk.ru/film/775276/", "https://www.kinopoisk.ru/film/977288/"]
dictionary2 = {"names_films": names_films, "types_film": types_films, "rating_films": rating_films, "years_films": years_films, "links_films": links_films}

df1 = pd.DataFrame(dictionary1)
df1.to_csv('micro_books.csv', index=False)
df2 = pd.DataFrame(dictionary2)
df2.to_csv('micro_films.csv', index=False)