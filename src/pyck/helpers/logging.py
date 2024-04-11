import logging
from logging.handlers import RotatingFileHandler
import traceback

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

    def error(
        self, message: str, additional_message: str = ""
    ) -> tuple[list[any], list[Exception]]:
        """Logs an ERROR message."""
        print(
            bold(red("\n-------------------- Error --------------------\n"))
            + bold(message)
        )
        self._logger.error(message)
        if additional_message:
            print("\n" + grey(additional_message))
            self._logger.error(additional_message)
        print(bold(red("-------------------- ----- --------------------\n")))

    def error_from_exception(self, exception: Exception):
        self.error(
            exception,
            additional_message="".join(
                traceback.format_exception(
                    type(exception),
                    value=exception,
                    tb=exception.__traceback__,
                )
            ),
        )
