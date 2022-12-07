import logging

def create_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.hasHandlers():

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

