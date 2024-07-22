import json
import logging

from config_data.config import config, MIN_LOG_LEVEL, LANG
from lexicon.lexicon import LEXICON


class Book:
    """Класс книги"""

    def __init__(self, title: str, author: str, year: int, status: bool = True) -> None:
        logger.debug(LEXICON[LANG]['init_book'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    @property
    def id(self) -> int:
        """Получение хэша книги"""
        logger.debug(LEXICON[LANG]['get_hash'])
        logger.debug(LEXICON[LANG]['book_details'].format(self.title, self.author, self.year))
        return hash((self.title, self.author, self.year))

    def __str__(self) -> str:
        """Строковое представление книги"""
        logger.debug(LEXICON[LANG]['get_string'])
        logger.debug(LEXICON[LANG]['book_details'].format(self.title, self.author, self.year))
        return (f"Название: {self.title}, автор: {self.author}, год издания: {self.year}. "
                f"Статус: {'выдана' if not self.status else 'в наличии'}")


class Library:
    """Класс библиотеки"""
    database = config.database_path + config.database_name
    library_object = None

    def __new__(cls, *args, **kwargs):
        logger.debug(LEXICON[LANG]['check_singleton'])
        if not cls.library_object:
            cls.library_object = super().__new__(cls)
        return cls.library_object

    def __init__(self) -> None:
        logger.info(LEXICON[LANG]['init_library'])
        self.books = {}
        self.load_library()

    @staticmethod
    def class_to_dict(book) -> dict:
        """Класс книги в словарь"""
        logger.debug(LEXICON[LANG]['book_to_dict'].format(book.__dict__))
        return book.__dict__

    def load_library(self) -> None:
        """Загрузка библиотеки из JSON файла"""
        logger.info(LEXICON[LANG]['load_from_json'])
        try:
            logger.debug(LEXICON[LANG]['load_raw_json'])
            with open(self.database, 'r') as file:
                result_json = json.load(file)
            logger.debug(LEXICON[LANG]['json_to_book'])
            for book_json in result_json.values():
                logger.debug(book_json)
                book = Book(book_json['title'], book_json['author'], book_json['year'], book_json['status'])
                self.books[book.id] = book
            logger.info(LEXICON[LANG]['library_loaded'])
        except (FileNotFoundError, json.JSONDecodeError):
            logger.warning(LEXICON[LANG]['error_load_library'])

    def save_library(self) -> None:
        """Сохранение библиотеки в JSON файл"""
        logger.info(LEXICON[LANG]['save_library'])
        with open(self.database, 'w') as file:
            json.dump(self.books, file, default=self.class_to_dict, ensure_ascii=False)

    @staticmethod
    def check_book_data(title: str = None, author: str = None, year: int = None) -> bool:
        """Проверка корректности данных для поиска книги"""
        logger.info(LEXICON[LANG]['check_book_data'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        if title and author and year:
            try:
                year = int(year)
                logger.info(LEXICON[LANG]['book_data_correct'].format(title, author, year))
                return True
            except ValueError:
                logger.info(LEXICON[LANG]['year_not_int'])
                return False
        else:
            logger.info(LEXICON[LANG]['book_data_incorrect'].format(title, author, year))
            return False

    def check_book(self, title: str = None, author: str = None, year: int = None) -> bool:
        """Проверка наличия книги в библиотеке"""
        logger.info(LEXICON[LANG]['check_book_in_library'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        if self.check_book_data(title, author, year):
            book_id = hash((title, author, year))
            if book_id in self.books:
                logger.info(LEXICON[LANG]['book_found'])
                return True
            else:
                logger.info(LEXICON[LANG]['book_not_found'].format(title, author, year))
                return False

    def search_books(self, title: str = None, author: str = None, year: str = None) -> list[Book]:
        """Поиск книг в библиотеке"""
        result = []
        logger.info(LEXICON[LANG]['book_search'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        for book in self.books.values():
            if title is None or title in book.title:
                if author is None or author in book.author:
                    if year is None or year in str(book.year):
                        logger.info(LEXICON[LANG]['book_found'])
                        result.append(book)
                    else:
                        logger.info(LEXICON[LANG]['book_not_found'].format(title, author, year))
        return result

    def add_book(self, title: str = None, author: str = None, year: int = None) -> None:
        """Добавление книги в библиотеку"""
        logger.info(LEXICON[LANG]['attempt_add_book'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        if self.check_book_data(title, author, year):
            book = Book(title, author, year)
            self.books[book.id] = book
            logger.info(LEXICON[LANG]['book_added'].format(title, author, year))

    def delete_book(self, title: str = None, author: str = None, year: int = None) -> None:
        """Удаление книги из библиотеки"""
        logger.info(LEXICON[LANG]['attempt_delete_book'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        if self.check_book_data(title, author, year):
            logger.info(LEXICON[LANG]['get_hash'])
            book_id = hash((title, author, year))
            if book_id in self.books:
                del self.books[book_id]
                logger.info(LEXICON[LANG]['book_deleted'])
            else:
                logger.info(LEXICON[LANG]['book_not_found'].format(title, author, year))

    def show_all_books(self) -> list[Book]:
        """Вывод всех книг в библиотеке"""
        logger.info(LEXICON[LANG]['show_all_books'])
        return list(self.books.values())

    def get_book(self, title: str = None, author: str = None, year: int = None) -> Book:
        """Получение данных книги из библиотеки"""
        logger.info(LEXICON[LANG]['get_book_data'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        if self.check_book_data(title, author, year):
            logger.info(LEXICON[LANG]['get_hash'])
            book_id = hash((title, author, year))
            if book_id in self.books:
                logger.info(LEXICON[LANG]['get_book_data_complete'])
                return self.books[book_id]
            else:
                logger.info(LEXICON[LANG]['book_not_found'].format(title, author, year))

    def get_status(self, title: str = None, author: str = None, year: int = None) -> bool:
        """Получение статуса книги"""
        logger.info(LEXICON[LANG]['get_book_status'])
        if self.check_book_data(title, author, year):
            book_id = hash((title, author, year))
            if book_id in self.books:
                logger.info(LEXICON[LANG]['get_book_status_complete'])
                return self.books[book_id].status
            else:
                logger.info(LEXICON[LANG]['book_not_found'].format(title, author, year))
                return False

    def change_status(self, title: str = None, author: str = None, year: int = None) -> None:
        """Изменение статуса книги"""
        logger.info(LEXICON[LANG]['change_book_status'])
        logger.debug(LEXICON[LANG]['book_details'].format(title, author, year))
        if self.check_book_data(title, author, year):
            logger.info(LEXICON[LANG]['get_hash'])
            book_id = hash((title, author, year))
            if book_id in self.books:
                self.books[book_id].status = not self.books[book_id].status
                logger.info(LEXICON[LANG]['change_book_status_complete'])
            else:
                logger.info(LEXICON[LANG]['book_not_found'].format(title, author, year))


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=MIN_LOG_LEVEL,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

# Инициализация библиотеки
library = Library()
