from db import Database
from prettytable import PrettyTable


def search_movies():
    db = Database()
    print("Введите команду:")
    print('- search "<keyword>" - поиск по ключевому слову')
    print('- search <genre> <year> - поиск по жанру и году')
    print("- history - показать популярные запросы")
    print("- exit - выход")

    while True:
        command = input("> ").strip()

        if command.lower() == "exit":
            print("Выход из программы.")
            break

        parts = command.split(maxsplit=1)
        if not parts:
            print("Некорректная команда. Попробуйте снова.")
            continue

        if parts[0] == "search":
            if len(parts) < 2:
                print("Некорректный ввод.")
                continue

            if parts[1].startswith('"') and parts[1].endswith('"'):
                keyword = parts[1][1:-1]
                movies = db.search_by_keyword(keyword)
                db.save_query(keyword)
                print_results(movies)
            else:
                args = parts[1].split()
                if len(args) == 2 and args[1].isdigit():
                    genre, year = args[0], args[1]
                    movies = db.search_by_genre_year(genre, int(year))
                    db.save_query(f"{genre} {year}")
                    print_results(movies)
                else:
                    print("Неверный формат запроса!")

        elif command.lower() == "history":
            queries = db.get_popular_queries()
            print("\nПопулярные запросы:")
            for q in queries:
                print(f"{q['query_text']} - {q['search_count']} раз")

        else:
            print("Неизвестная команда.")

    db.close()


def print_results(movies):
    if not movies:
        print("Фильмы не найдены.")
        return

    table = PrettyTable(["Название", "Год", "Жанр"])
    for movie in movies:
        genre = movie.get('genre', 'Неизвестный жанр')
        table.add_row([movie['title'], movie['release_year'], genre])

    print(table)
