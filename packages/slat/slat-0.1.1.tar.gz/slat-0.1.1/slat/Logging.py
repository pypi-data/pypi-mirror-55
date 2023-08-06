import logging
import os


class Logging:

    @staticmethod
    def init_logger() -> logging.Logger:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logger = logging.getLogger()
        logger.setLevel(log_level)
        return logger
