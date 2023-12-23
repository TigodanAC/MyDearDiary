import pandas as pd
from transliterate import translit

def id_maker_books(ru_name, year):
    en_name = translit(ru_name, language_code='ru', reversed=True).lower()
    return (en_name+" "+year).replace(' ', '_')

def id_maker_films(ru_name, ru_author):
    en_name = translit(ru_name, language_code='ru', reversed=True).lower()
    en_author = translit(ru_author, language_code='ru', reversed=True).lower()
    return (en_name+" "+en_author).replace(' ', '_')


names_books = ["Бесы", "Шах и мат"]
types_books = ["Классическая русская литература", "Современные любовные романы"]
authors_books =["Достоевский Федор Михайлович", "Хейзелвуд Али"]
rating_books = [4.7, 4.4]
links_books = ["https://book24.ru/product/besy-5422017/", "https://book24.ru/product/shakh-i-mat-6784435/"]
id_books = [id_maker_books(names_books[0], authors_books[0]), id_maker_books(names_books[1], authors_books[1])]
dictionary1 = {"id_books": id_books, "names_books": names_books, "authors_books": authors_books, "types_books": types_books, "rating_books": rating_books, "links_books": links_books}


names_films = ["Зверополис", "Поезд в Пусан"]
types_films = ["Мультфильм", "Ужасы, Боевик"]
years_films = ["2016", "2016"]
id_films = [id_maker_films(names_films[0], years_films[0]), id_maker_films(names_films[1], years_films[1])]
rating_films = [8.3, 7.2]
links_films = ["https://www.kinopoisk.ru/film/775276/", "https://www.kinopoisk.ru/film/977288/"]
dictionary2 = {"id_films": id_films, "names_films": names_films, "types_film": types_films, "rating_films": rating_films, "years_films": years_films, "links_films": links_films}

df1 = pd.DataFrame(dictionary1)
df1.to_csv('micro_books.csv', index=False)
df2 = pd.DataFrame(dictionary2)
df2.to_csv('micro_films.csv', index=False)