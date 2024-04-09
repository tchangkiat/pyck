import logging
from logging.handlers import RotatingFileHandler

from pyck.utils.styles import red, grey, bold


class Logging(object):
    _instance = None

    _formatter = logging.Formatter(
        "[%(asctime)s %(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    _logger = logging.getLogger("default")
    _logger.setLevel(logging.INFO)
    _fh = RotatingFileHandler("app.log", maxBytes=1024 * 1024 * 1, backupCount=3)
    _fh.setLevel(logging.INFO)
    _fh.setFormatter(_formatter)
    _logger.addHandler(_fh)

    @classmethod
    def get_instance(cls):
        """Get the instance of the logging object, or create one if not created yet"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def info(self, message: str):
        """Logs an INFO message."""
        print(message)
        self._logger.info(message)

    def debug(self, message: str):
        """Logs a debug message."""
        print(grey(message))
        self._logger.info(message)

    def error(self, message: str, additional_message: str = ""):
        """Logs an ERROR message."""
        print(
            bold(red("\n-------------------- Error --------------------\n"))
            + bold(message)
        )
        if additional_message:
            print("\n" + additional_message)
            self._logger.error(additional_message)
        print(bold(red("-------------------- ----- --------------------\n")))
        self._logger.error(message)
