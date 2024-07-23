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
    """ Запрос выбора пункта меню """
    logger.debug(LEXICON[LANG]['request_menu_command'])
    while True:
        print()
        print(LEXICON[LANG]['menu_top'])
        print(LEXICON[LANG]['-'])
        print(LEXICON[LANG]['1_add_book'])
        print(LEXICON[LANG]['2_delete_book'])
        print(LEXICON[LANG]['3_search_book'])
        print(LEXICON[LANG]['4_show_all_books'])
        print(LEXICON[LANG]['5_change_book_status'])
        print(LEXICON[LANG]['6_shutdown'])
        print(LEXICON[LANG]['-'])

        command = input(LEXICON[LANG]['choice_menu_item'])
        try:
            command = int(command)
            logger.debug(LEXICON[LANG]['choice_menu_item_complete'].format(command))
            return command
        except ValueError:
            logger.debug(LEXICON[LANG]['incorrect_choice_menu_item'].format(command))
            print(LEXICON[LANG]['not_int'])


def new_book_data() -> tuple:
    """ Запрос корректных данных о новой книге """
    logger.info(LEXICON[LANG]['new_book_data'])
    while True:
        while True:
            title = input(LEXICON[LANG]['enter_book_title'])
            if title:
                break
            logger.debug(LEXICON[LANG]['no_book_title'])
            print(LEXICON[LANG]['book_title_not_entered'])
        while True:
            author = input(LEXICON[LANG]['enter_author_name'])
            if author:
                break
            logger.debug(LEXICON[LANG]['no_author_name'])
            print(LEXICON[LANG]['author_name_not_entered'])
        while True:
            year = input(LEXICON[LANG]['enter_book_year'])
            try:
                year = int(year)
                break
            except ValueError:
                logger.debug(LEXICON[LANG]['year_not_valid'].format(year))
                print(LEXICON[LANG]['not_int'])
        break
    logger.info(LEXICON[LANG]['all_values_entered'].format(title, author, year))
    return title, author, year


def add_book():
    """ Добавление книги в библиотеку """
    logger.info(LEXICON[LANG]['1_add_book'])
    print(LEXICON[LANG]['1_add_book'])
    print(LEXICON[LANG]['-'])
    book = new_book_data()
    result = library.add_book(*book)
    if result == 0:
        logger.info(LEXICON[LANG]['book_added'])
        print(LEXICON[LANG]['book_added'])
    elif result == 1:
        logger.info(LEXICON[LANG]['book_exist'])
        print(LEXICON[LANG]['book_exist'])
    else:
        logger.info(LEXICON[LANG]['book_not_added'])
        print(LEXICON[LANG]['book_not_added'])


def delete_book():
    """ Удаление книги по ID """
    logger.info(LEXICON[LANG]['2_delete_book'])
    print(LEXICON[LANG]['2_delete_book'])
    print(LEXICON[LANG]['-'])
    while True:
        book_id = input(LEXICON[LANG]['enter_book_id'])
        try:
            book_id = int(book_id)
            logger.info(LEXICON[LANG]['book_id_entered'].format(book_id))
            break
        except ValueError:
            logger.debug(LEXICON[LANG]['incorrect_book_id_entered'].format(book_id))
            print(LEXICON[LANG]['not_int'])
    if library.check_book_id(book_id):
        library.delete_book(book_id)
        logger.info(LEXICON[LANG]['book_deleted'].format(book_id))
        print(LEXICON[LANG]['book_deleted'].format(book_id))
    else:
        logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))
        print(LEXICON[LANG]['book_with_id_not_found'].format(book_id))


def search_book():
    """ Поиск книги параметрам title, author, year """
    logger.info(LEXICON[LANG]['3_search_book'])
    print(LEXICON[LANG]['3_search_book'])
    print(LEXICON[LANG]['-'])
    title = input(LEXICON[LANG]['enter_book_title_or_empty'])
    author = input(LEXICON[LANG]['enter_author_name_or_empty'])
    while True:
        year = input(LEXICON[LANG]['enter_book_year_or_empty'])
        try:
            year = int(year)
            break
        except ValueError:
            logger.debug(LEXICON[LANG]['not_int'])
            print(LEXICON[LANG]['not_int'])
        break
    logger.info(LEXICON[LANG]['all_values_entered'].format(title, author, year))
    logger.info(LEXICON[LANG]['start_books_search'])
    result = library.search_books(title, author, year)
    if result:
        logger.info(LEXICON[LANG]['show_books_list'])
        print(LEXICON[LANG]['show_books_list'])
        print(LEXICON[LANG]['-'])
        print(*result, sep='\n')
    else:
        logger.info(LEXICON[LANG]['empty_search_results'])
        print(LEXICON[LANG]['empty_search_results'])


def show_all_books():
    """ Показать все книги """
    logger.info(LEXICON[LANG]['4_show_all_books'])
    print(LEXICON[LANG]['4_show_all_books'])
    print(LEXICON[LANG]['-'])
    result = library.show_all_books()
    if result:
        print(*result, sep='\n')
        print()
    else:
        print(LEXICON[LANG]['library_is_empty'])


def change_status():
    """ Изменение статуса книги """
    logger.info(LEXICON[LANG]['5_change_book_status'])
    print(LEXICON[LANG]['5_change_book_status'])
    print(LEXICON[LANG]['-'])
    while True:
        book_id = input(LEXICON[LANG]['enter_book_id'])
        try:
            book_id = int(book_id)
            break
        except ValueError:
            logger.debug(LEXICON[LANG]['incorrect_book_id_entered'].format(book_id))
            print(LEXICON[LANG]['not_int'])
    if library.check_book_id(book_id):
        book_info = library.get_book_details(book_id)
        print(LEXICON[LANG]['book_details'].format(book_id, book_info[0], book_info[1], book_info[2], book_info[3]))
        while True:
            choice_new_status = input(LEXICON[LANG]['change_book_status'])
            if choice_new_status.lower() in LEXICON[LANG]['yes'].split():
                if book_info[3] == LEXICON[LANG]['in_library']:
                    new_status = LEXICON[LANG]['not_in_library']
                else:
                    new_status = LEXICON[LANG]['in_library']
                library.change_status(book_id, new_status)
                logger.info(LEXICON[LANG]['book_status_changed'].format(book_id, new_status))
                print(LEXICON[LANG]['book_status_changed'].format(book_id, new_status))
                break
            elif choice_new_status in LEXICON[LANG]['no']:
                logger.info(LEXICON[LANG]['book_status_not_changed'].format(book_id))
                print(LEXICON[LANG]['book_status_not_changed'].format(book_id))
                break
            else:
                logger.debug(LEXICON[LANG]['incorrect_yes_no'])
                print(LEXICON[LANG]['incorrect_yes_no'])
    else:
        logger.info(LEXICON[LANG]['book_with_id_not_found'].format(book_id))
        print(LEXICON[LANG]['book_with_id_not_found'].format(book_id))


def shutdown():
    logger.info(LEXICON[LANG]['6_shutdown'])
    library.save_library()
    logger.info(LEXICON[LANG]['program_stopped'])
    raise SystemExit
