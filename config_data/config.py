import logging
from dataclasses import dataclass

from environs import Env
from lexicon.lexicon import LEXICON

MIN_LOG_LEVEL = logging.DEBUG
LANG = 'RU'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=MIN_LOG_LEVEL,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


@dataclass
class Config:
    database_name: str
    database_path: str


def load_config(path: str | None = None) -> Config:
    logger.info(LEXICON[LANG]['env_load'])
    try:
        env: Env = Env()
        env.read_env(path)
        logger.info(LEXICON[LANG]['env_load_complete'])
        return Config(
            database_name=env('database_name'),
            database_path=env('database_path')
        )

    except FileNotFoundError:
        logger.critical(LEXICON[LANG]['env_load_error'])
        return Config(
            database_name='database.db',
            database_path=''
        )


config = load_config('.env')
