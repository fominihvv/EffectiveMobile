import json
import logging

from config_data.config import config, MIN_LOG_LEVEL, LANG
from lexicon.lexicon import LEXICON


class Book:
    """Класс книги"""

    def __init__(self, title: str, author: str, year: int, book_id: int = None, status: str = 'в наличии') -> None:
        logger.debug(LEXICON[LANG]['init_book'])
        logger.debug(LEXICON[LANG]['book_details'].format(book_id, title, author, year, status))
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.id = book_id

    def __str__(self) -> str:
        """Строковое представление книги"""
        logger.debug(LEXICON[LANG]['get_string'])
        logger.debug(LEXICON[LANG]['book_details'].format(self.id, self.title, self.author, self.year, self.status))
        return LEXICON[LANG]['book_details'].format(self.id, self.title, self.author, self.year, self.status)


class Library:
    """Класс библиотеки"""
    database = config.database_path + config.database_name
    library_object = None
    NEXT_ID = 1

    def __new__(cls, *args, **kwargs):
        logger.debug(LEXICON[LANG]['check_singleton'])
        if not cls.library_object:
            logger.debug(LEXICON[LANG]['create_singleton'])
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
        logger.info(LEXICON[LANG]['load_raw_json'])
        try:
            logger.debug(LEXICON[LANG]['load_from_raw'])
            with open(self.database, 'r', encoding='utf-8') as file:
                result_json = json.load(file)
            logger.debug(LEXICON[LANG]['json_to_book'])
            for book_json in result_json.values():
                book = Book(book_json['title'], book_json['author'], book_json['year'], book_json['id'],
                            book_json['status'])
                logger.debug(LEXICON[LANG]['book_added'])
                logger.debug(
                    LEXICON[LANG]['book_details'].format(book.id, book.title, book.author, book.year, book.status))
                self.books[book.id] = book
                if book.id > self.NEXT_ID:
                    self.NEXT_ID = book.id
            self.NEXT_ID += 1
            logger.info(LEXICON[LANG]['library_loaded'])
        except Exception:
            logger.warning(LEXICON[LANG]['error_load_library'])

    def save_library(self) -> None:
        """Сохранение библиотеки в JSON файл"""
        logger.info(LEXICON[LANG]['save_library'])
        with open(self.database, 'w', encoding='utf-8') as file:
            json.dump(self.books, file, default=self.class_to_dict, ensure_ascii=False)

    @staticmethod
    def check_book_data(title: str = None, author: str = None, year: int = None) -> bool:
        """Проверка корректности данных для книги"""
        logger.info(LEXICON[LANG]['check_book_data'])
        logger.debug(LEXICON[LANG]['book_details'].format('---', title, author, year, '---'))
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
        """Проверка наличия книги по данным"""
        logger.info(LEXICON[LANG]['check_book_in_library'])
        logger.debug(LEXICON[LANG]['book_details'].format('---', title, author, year, '---'))
        for book in self.books.values():
            if title == book.title and author == book.author and year == book.year:
                logger.info(LEXICON[LANG]['book_with_data_found'].format(title, author, year))
                return True
        logger.info(LEXICON[LANG]['book_with_data_not_found'].format(title, author, year))
        return False

    def check_book_id(self, book_id: int) -> bool:
        """Проверка наличия книги по ID"""
        logger.info(LEXICON[LANG]['check_book_id'].format(book_id))
        if book_id in self.books:
            logger.info(LEXICON[LANG]['book_with_id_found'].format(book_id))
            return True
        else:
            logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))
            return False

    def search_books(self, title: str = None, author: str = None, year: str = None) -> list[Book]:
        """Поиск книг в библиотеке"""
        result = []
        logger.info(LEXICON[LANG]['book_search'])
        logger.debug(LEXICON[LANG]['book_details'].format('---', title, author, year, '---'))
        for book in self.books.values():
            if title is None or title in book.title:
                if author is None or author in book.author:
                    if year is None or year in str(book.year):
                        logger.info(LEXICON[LANG]['book_with_data_found'].format(title, author, year))
                        result.append(book)
                    else:
                        logger.info(LEXICON[LANG]['book_with_data_not_found'].format(title, author, year))
        return result

    def add_book(self, title: str = None, author: str = None, year: int = None) -> None:
        """Добавление книги в библиотеку"""
        logger.info(LEXICON[LANG]['attempt_add_book'])
        logger.debug(LEXICON[LANG]['book_details'].format('---', title, author, year, '---'))
        if self.check_book_data(title, author, year):
            book = Book(title, author, year)
            book.id = self.NEXT_ID
            self.NEXT_ID += 1
            self.books[book.id] = book
            logger.info(LEXICON[LANG]['book_added'])
            logger.info(LEXICON[LANG]['book_details'].format(book.id, book.title, book.author, book.year, book.status))

    def delete_book(self, book_id: int) -> None:
        """Удаление книги из библиотеки"""
        logger.info(LEXICON[LANG]['attempt_delete_book'])
        if self.check_book_id(book_id):
            logger.info(LEXICON[LANG]['book_with_id_found'].format(book_id))
            del self.books[book_id]
            logger.info(LEXICON[LANG]['book_deleted'])
        else:
            logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))

    def show_all_books(self) -> list[Book]:
        """Вывод всех книг в библиотеке"""
        logger.info(LEXICON[LANG]['show_all_books'])
        return list(self.books.values())

    def get_status(self, book_id: int) -> str | None:
        """Получение статуса книги"""
        logger.info(LEXICON[LANG]['get_book_status'])
        if book_id in self.books:
            logger.info(LEXICON[LANG]['get_book_status_complete'])
            return self.books[book_id].status
        else:
            logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))
            return None

    def get_book_details(self, book_id: int) -> tuple | None:
        """Получение детальной информации о книге"""
        logger.info(LEXICON[LANG]['get_book_data'])
        if book_id in self.books:
            logger.info(LEXICON[LANG]['book_with_id_found'].format(book_id))
            logger.info(
                LEXICON[LANG]['book_details'].format(book_id, self.books[book_id].title, self.books[book_id].author,
                                                     self.books[book_id].year, self.books[book_id].status))
            return self.books[book_id].title, self.books[book_id].author, self.books[book_id].year, self.books[book_id].status
        else:
            logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))
            return None

    def change_status(self, book_id: int, status: str) -> None:
        """Изменение статуса книги"""
        logger.info(LEXICON[LANG]['change_status'])
        if book_id in self.books:
            self.books[book_id].status = status
            logger.info(LEXICON[LANG]['change_book_status_complete'])
        else:
            logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=MIN_LOG_LEVEL,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

# Инициализация библиотеки
library = Library()
