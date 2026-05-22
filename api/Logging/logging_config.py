import logging
import os 

def configure_user_logging(user_id, level=logging.INFO):
    if not os.path.exists('Logs'):
        os.makedirs('Logs')

    log_file = f'Logs/{user_id}.log'

    logger = logging.getLogger(user_id)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
    return logger