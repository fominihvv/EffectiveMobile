import logging

from biblioteka.services import library
from config_data.config import MIN_LOG_LEVEL, LANG
from lexicon.lexicon import LEXICON

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=MIN_LOG_LEVEL,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


def get_menu_command() -> int:
    logger.debug('Запрос пункта меню управления библиотекой')
    while True:
        print('МЕНЮ управления библиотекой:')
        print('----------------------------')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Поиск книги')
        print('4. Отображение всех книг')
        print('5. Изменить статус книги')
        print('6. Выход')
        print('----------------------------')

        command = input('Выберите пункт меню: ')
        try:
            command = int(command)
            logger.debug(f'Пользователь выбрал пункт меню {command}')
            return command
        except ValueError:
            logger.debug(f'Неверное значение. Пользователь пытался выбрать пункт меню {command}')
            print('Неверное значение. Пожалуйста, введите целое число.')


def get_book_id() -> tuple:
    logger.info(LEXICON[LANG]['new_book_data'])
    while True:
        while True:
            title = input('Введите название книги: ')
            if not title:
                logger.debug(LEXICON[LANG]['no_book_name'])
                print('Название книги не введено. Пожалуйста, введите название книги.')
            break
        while True:
            author = input('Введите автора книги: ')
            if not author:
                logger.debug(LEXICON[LANG]['no_author_name'])
                print('Автор книги не введен. Пожалуйста, введите название книги.')
            break
        while True:
            try:
                year = int(input('Введите год издания книги: '))
                break
            except ValueError:
                logger.debug('Неверное значение. Пользователь пытался ввести год издания книги')
                print('Неверное значение. Пожалуйста, введите целое число.')

        break
    logger.info(f'Все данные введены корректно. Название книги: {title}, автор книги: {author}, год издания: {year}')

    return title, author, year


def add_book():
    logger.info('Добавление книги в библиотеку')
    print('Добавление книги в библиотеку')
    print('----------------------------')
    book = get_book_id()
    if library.check_book(*book):
        logger.info(LEXICON[LANG]['book_exist'])
        logger.info(LEXICON[LANG]['book_details'].format(*book))
        print(f'Книга {book} уже есть в библиотеке\n')
    else:
        library.add_book(*book)
        print(f'Книга {book} добавлена в библиотеку\n')


def delete_book():
    logger.info('Удаление книги из библиотеки')
    print('Удаление книги из библиотеки')
    print('----------------------------')
    book = get_book_id()
    if not library.check_book(*book):
        logger.info(f'Книги {book} нет в библиотеке')
        print(f'Книги {book} нет в библиотеке\n')
    else:
        library.delete_book(*book)
        print(f'Книга {book} удалена из библиотеки\n')


def search_book():
    logger.info('Поиск книги в библиотеке')
    print('Поиск книги в библиотеке')
    print('----------------------------')
    title = input('Введите название книги, либо оставьте поле пустым: ')
    author = input('Введите автора книги, либо оставьте поле пустым: ')
    while True:
        try:
            year = input('Введите год издания книги, либо оставьте поле пустым: ')
            logger.info(
                f'Все данные введены корректно. Название книги: {title}, автор книги: {author}, год издания: {year}')
            break
        except ValueError:
            logger.debug('Неверное значение. Пользователь пытался ввести год издания книги')
            print('Неверное значение. Пожалуйста, введите целое число.')
        break
    logger.info(f'Поиск книг в библиотеке. Название книги: {title}, автор книги: {author}, год издания: {year}')
    result = library.search_books(title, author, year)
    if result:
        logger.info('Вывод списка книг')
        print('Вывод списка книг')
        print('----------------------------')
        print(*result, sep='\n')
        print()
    else:
        logger.info('Подходящие ниги не найдены')
        print('Подходящие книги не найдены\n')


def show_all_books():
    logger.info('Показать все книги')
    print('Показать все книги')
    print('----------------------------')
    result = library.show_all_books()
    print(*result, sep='\n')
    print()


def change_status():
    logger.info('Изменение статуса книги')
    book = get_book_id()
    if not library.check_book(*book):
        logger.info(LEXICON[LANG]['book_not_found'].format(*book))
        print('Такой книги нет в библиотеке\n')
    else:
        logger.info(f'Статус книги изменён')
        print('Статус книги:', ['выдана', 'в наличии'][library.get_status(*book)], end='')
        library.change_status(*book)
        print('изменён на ', ['выдана', 'в наличии'][library.get_status(*book)])
        print()


def shutdown():
    logger.info('Выход из программы')
    library.save_library()
    raise SystemExit
