import json
from dataclasses import dataclass


@dataclass
class Book:
    """Класс книги"""
    title: str
    author: str
    year: int
    status: bool = 'В наличии'

    def __post_init__(self):
        self.id = hash((self.title, self.author, self.year))


class Biblioteka:
    """Класс библиотеки"""
    database = 'biblioteka.json'

    def __init__(self) -> None:
        self.books = self.load_biblioteka()

    def class_to_dict(self, book) -> dict:
        """Класс книги в словарь"""
        return book.__dict__

    def load_biblioteka(self) -> dict:
        """Загрузка библиотеки из JSON файла"""
        try:
            with open(self.database, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_biblioteka(self) -> None:
        """Сохранение библиотеки в JSON файл"""
        with open(self.database, 'w') as file:
            json.dump(self.books, file, default=self.class_to_dict)

    def check_book(self, book: Book) -> bool:
        """Проверка наличия книги в библиотеке"""
        if isinstance(book, Book):
            return book.id in self.books
        return False

    def search_book(self) -> None:
        """Поиск книги в библиотеке"""
        pass

    def add_book(self, book: Book) -> None:
        """Добавление книги в библиотеку"""
        if isinstance(book, Book):
            if book.id not in self.books:
                self.books[book.id] = book
        pass

    def delete_book(self) -> None:
        """Удаление книги из библиотеки"""
        pass

    def show_books(self) -> None:
        """Вывод всех книг в библиотеке"""
        if self.books:
            for book in self.books:
                print(f'{book["title"]} - {book["author"]} - {book["year"]}')
        else:
            print('Библиотека пуста')

    def change_status(self):
        """Изменение статуса книги"""
        pass


biblioteka = Biblioteka()
