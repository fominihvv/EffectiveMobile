import logging

from config_data.config import MIN_LOG_LEVEL, LANG
from lexicon.lexicon import LEXICON
from menu import menu


def run():
    while True:
        logger.info(LEXICON[LANG]['await_command'])
        command = menu.get_menu_command()
        match command:
            case 1:
                logger.info(LEXICON[LANG]['call_book_add'])
                menu.add_book()
            case 2:
                logger.info(LEXICON[LANG]['call_book_delete'])
                menu.delete_book()
            case 3:
                logger.info(LEXICON[LANG]['call_book_search'])
                menu.search_book()
            case 4:
                logger.info(LEXICON[LANG]['call_show_all_books'])
                menu.show_all_books()
            case 5:
                logger.info(LEXICON[LANG]['call_change_book_status'])
                menu.change_status()
            case 6:
                logger.info(LEXICON[LANG]['call_shutdown'])
                menu.shutdown()


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=MIN_LOG_LEVEL,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

logger.info(LEXICON[LANG]['program_start'])

if __name__ == '__main__':
    run()
