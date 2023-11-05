"""Configures logger, creates folder for log files."""
import json
import logging
import logging.config
import os

FOLDER_LOG = os.path.join(os.environ.get('ROOT_PATH'), 'sqlite_to_postgres/log')
LOGGING_CONFIG_FILE = os.path.join(os.environ.get('ROOT_PATH'), 'sqlite_to_postgres/logger.json')


def create_log_folder(folder=FOLDER_LOG) -> None:
    """Create folder for log files.

    Args:
        folder: folder path
    """
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name, template='default') -> logging.Logger:
    """Configure logger.

    Args:
        name: logger name
        template: template

    Returns:
            logging.Logger: configured logger
    """
    create_log_folder()
    with open(LOGGING_CONFIG_FILE, 'r') as f:
        dict_config = json.load(f)
        dict_config.get('handlers').get('rotating_file').update({'filename': os.path.join(FOLDER_LOG, 'main.log')})
        dict_config['loggers'][name] = dict_config['loggers'][template]
    logging.config.dictConfig(dict_config)
    return logging.getLogger(name)
