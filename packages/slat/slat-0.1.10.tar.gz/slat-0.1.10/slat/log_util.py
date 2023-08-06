import logging
import os
import sys
from typing import Dict

import structlog

# configured for JSON logging
# see: http://www.structlog.org/en/stable/standard-library.html#rendering-within-structlog

structlog.configure(
    processors=[
        # This performs the initial filtering, so we don't
        # evaluate e.g. DEBUG when unnecessary
        structlog.stdlib.filter_by_level,
        # Adds logger=module_name (e.g __main__)
        structlog.stdlib.add_logger_name,
        # Adds level=info, debug, etc.
        structlog.stdlib.add_log_level,
        # Performs the % string interpolation as expected
        structlog.stdlib.PositionalArgumentsFormatter(),
        # add ISO9601 stamp: e.g. 2019-11-06T19:53:41.189600Z
        structlog.processors.TimeStamper(fmt="iso"),
        # Include the stack when stack_info=True
        structlog.processors.StackInfoRenderer(),
        # Include the exception when exc_info=True
        # e.g log.exception() or log.warning(exc_info=True)'s behavior
        structlog.processors.format_exc_info,
        # Decodes the unicode values in any kv pairs
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(sort_keys=True)
    ],
    # Our "event_dict" is explicitly a dict
    # There's also structlog.threadlocal.wrap_dict(dict) in some examples
    # which keeps global context as well as thread locals
    context_class=dict,
    # Provides the logging.Logger for the underlaying log call
    logger_factory=structlog.stdlib.LoggerFactory(),
    # Provides predefined methods - log.debug(), log.info(), etc.
    wrapper_class=structlog.stdlib.BoundLogger,
    # Caching of our logger
    cache_logger_on_first_use=True,
)


class LogUtil:

    @staticmethod
    def init_logger(env_var_name: str = 'LOG_LEVEL',
                    default_level: str = 'INFO',
                    correlation_id_key_val: Dict[str, str] = None) -> logging.Logger:
        """

        :param correlation_id_key_val: [optional] correlation {key: val} to appear in all log statements.
        :type correlation_id_key_val: str
        :param env_var_name: [optional] Looks for log level [DEBUG|INFO|...] set at this ENV var name
        :type env_var_name: str
        :param default_level: [optional, defaults to INFO] Run this level if env_var_name not found
        :type default_level: str
        :return:
        :rtype: Logging.Logger
        """

        # remove the Lambda build handles.
        # https://stackoverflow.com/questions/37703609/using-python-logging-with-aws-lambda
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)

        log_level = os.getenv(env_var_name, default_level)
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=log_level.upper(),
        )
        log = structlog.getLogger()
        # @TODO gotta be a better way to do this??
        if os.getenv('TESTING_RUN', False):
            fh = logging.FileHandler('testing.log')
            log.addHandler(fh)
        if correlation_id_key_val:
            log = log.bind(**correlation_id_key_val)
        return log

    @staticmethod
    def bind(key_val: Dict[str, str]) -> logging.Logger:
        return structlog.getLogger().bind(**key_val)
